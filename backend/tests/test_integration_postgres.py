"""Safety-gated PostgreSQL integration tests."""
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from threading import Barrier, BrokenBarrierError
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "").strip()

def _target_id(url: str) -> tuple[str, str, int, str, str] | None:
    parsed = urlsplit(url)
    if not parsed.scheme or not parsed.hostname or not parsed.path:
        return None
    return (parsed.scheme.lower(), parsed.hostname.lower(), parsed.port or 5432, parsed.path.lstrip("/").lower(), (parsed.username or "").lower())

def _safe_test_database(url: str) -> tuple[bool, str]:
    if not url: return False, "TEST_DATABASE_URL is not configured"
    parsed = urlsplit(url); host = (parsed.hostname or "").lower()
    if parsed.scheme != "postgresql+psycopg": return False, "TEST_DATABASE_URL must use postgresql+psycopg"
    if host != "127.0.0.1" or (parsed.port or 5432) != 5434: return False, "TEST_DATABASE_URL must target isolated PostgreSQL at 127.0.0.1:5434"
    if any(marker in (parsed.path or "").lower() for marker in ("prod", "production", "main")): return False, "production-like database name rejected"
    try:
        from app.core.config import get_settings
        application_url = get_settings().database_url
    except Exception:
        return False, "application configuration could not be resolved safely"
    if _target_id(url) == _target_id(application_url): return False, "TEST_DATABASE_URL must not target the application database"
    return True, ""

SAFE_DATABASE, SAFETY_REASON = _safe_test_database(TEST_DATABASE_URL)
pytestmark = pytest.mark.skipif(not SAFE_DATABASE, reason=SAFETY_REASON)

if SAFE_DATABASE:
    from app.core.security import hash_password
    from app.db.session import get_db
    from app import main as main_module
    from app.main import app
    from app.models import User, UserRole
    from app.models import Event, EventStatus, Registration, RegistrationStatus, Venue
    from app.schemas.event import EventCreate
    from app.services import event_service, registration_service
    test_engine = create_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10, "options": "-c lock_timeout=10000 -c statement_timeout=15000"},
    )

@pytest.fixture()
def db_session():
    connection = test_engine.connect(); transaction = connection.begin(); session = Session(bind=connection, expire_on_commit=False, join_transaction_mode="create_savepoint")
    try: yield session
    finally: session.close(); transaction.rollback(); connection.close()

@pytest.fixture()
def client(db_session):
    def override_get_db(): yield db_session
    app.dependency_overrides[get_db] = override_get_db
    original_engine = main_module.engine
    main_module.engine = test_engine
    try:
        with TestClient(app) as test_client: yield test_client
    finally:
        app.dependency_overrides.clear()
        main_module.engine = original_engine

def _register(client, email=None):
    email = email or f"user-{uuid4().hex}@example.com"
    response = client.post("/api/auth/register", json={"email": email, "password": "ValidPass123!"})
    assert response.status_code == 201, f"registration failed: status={response.status_code} body={response.json()}"
    return response.json(), email

def _admin(db_session):
    user = User(email=f"admin-{uuid4().hex}@example.com", password_hash=hash_password("AdminPass123!"), role=UserRole.ADMIN)
    db_session.add(user); db_session.commit(); db_session.refresh(user); return user

def _venue(client, token, capacity=50):
    response = client.post("/api/venues", headers={"Authorization": f"Bearer {token}"}, json={"name": f"Venue {uuid4().hex}", "capacity": capacity, "location": "Test location"})
    assert response.status_code == 201; return response.json()

def _event(client, token, venue_id, status="PUBLISHED", capacity=10, start_offset_days=0):
    start = datetime.now(timezone.utc) + timedelta(days=2 + start_offset_days, hours=1)
    response = client.post("/api/events", headers={"Authorization": f"Bearer {token}"}, json={"title": f"Event {uuid4().hex}", "venue_id": venue_id, "starts_at": start.isoformat(), "ends_at": (start + timedelta(hours=2)).isoformat(), "capacity": capacity, "status": status})
    try:
        body = response.json()
    except ValueError:
        body = {"raw": response.text[:500]}
    assert response.status_code == 201, f"event creation failed: status={response.status_code} body={body}"
    return body

def test_registration_login_and_duplicate_email(client):
    _, email = _register(client)
    assert client.post("/api/auth/register", json={"email": email.upper(), "password": "ValidPass123!"}).status_code == 409
    login = client.post("/api/auth/login", json={"email": email, "password": "ValidPass123!"})
    assert login.status_code == 200; assert login.json()["access_token"]; assert "password_hash" not in login.json()["user"]

def test_authentication_and_user_restrictions(client):
    user, _ = _register(client); token = user["access_token"]; headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/auth/me", headers=headers).status_code == 200
    assert client.get("/api/venues", headers=headers).status_code == 200
    assert client.post("/api/venues", headers=headers, json={"name": "Denied", "capacity": 1, "location": "x"}).status_code == 403

def test_admin_venue_event_and_published_visibility(client, db_session):
    admin = _admin(db_session); token = client.post("/api/auth/login", json={"email": admin.email, "password": "AdminPass123!"}).json()["access_token"]
    venue = _venue(client, token); published = _event(client, token, venue["id"], "PUBLISHED"); draft = _event(client, token, venue["id"], "DRAFT", start_offset_days=1)
    listed = client.get("/api/events"); ids = {item["id"] for item in listed.json()}
    assert listed.status_code == 200; assert published["id"] in ids; assert draft["id"] not in ids; assert client.get(f"/api/events/{draft['id']}").status_code == 404

def test_registration_duplicate_capacity_and_cancellation(client, db_session):
    admin = _admin(db_session); admin_token = client.post("/api/auth/login", json={"email": admin.email, "password": "AdminPass123!"}).json()["access_token"]
    event = _event(client, admin_token, _venue(client, admin_token, 2)["id"], capacity=1)
    participant, _ = _register(client); headers = {"Authorization": f"Bearer {participant['access_token']}"}
    assert client.post(f"/api/events/{event['id']}/register", headers=headers).status_code == 201
    assert client.post(f"/api/events/{event['id']}/register", headers=headers).status_code == 409
    other, _ = _register(client)
    assert client.post(f"/api/events/{event['id']}/register", headers={"Authorization": f"Bearer {other['access_token']}"}).status_code == 409
    assert client.delete(f"/api/events/{event['id']}/register", headers=headers).status_code == 200

def test_invalid_token_and_validation_error_contract(client):
    invalid = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid"})
    assert invalid.status_code == 401; assert invalid.json()["error"]["code"] == "HTTP_401"
    body = client.post("/api/auth/register", json={"email": "bad", "password": "x"})
    assert body.status_code == 422; assert body.json()["error"]["code"] == "VALIDATION_ERROR"

def test_expired_token_is_rejected(client):
    from app.core.security import decode_access_token
    from app.core.config import get_settings
    import jwt
    token = jwt.encode({"sub": str(uuid4()), "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}, get_settings().jwt_secret_key, algorithm=get_settings().jwt_algorithm)
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_profile_update_and_duplicate_email_conflict(client):
    first, first_email = _register(client); second, second_email = _register(client)
    headers = {"Authorization": f"Bearer {first['access_token']}"}
    updated = client.patch("/api/users/me", headers=headers, json={"email": f"updated-{uuid4().hex}@example.com"})
    assert updated.status_code == 200 and updated.json()["email"].startswith("updated-")
    conflict = client.patch("/api/users/me", headers=headers, json={"email": second_email})
    assert conflict.status_code == 409

def test_venue_update_availability_and_overlap_rejection(client, db_session):
    admin = _admin(db_session); token = client.post("/api/auth/login", json={"email": admin.email, "password": "AdminPass123!"}).json()["access_token"]
    venue = _venue(client, token); event = _event(client, token, venue["id"])
    updated = client.patch(f"/api/venues/{venue['id']}", headers={"Authorization": f"Bearer {token}"}, json={"location": "Updated location"})
    assert updated.status_code == 200
    start = datetime.fromisoformat(event["starts_at"])
    availability = client.get(f"/api/venues/{venue['id']}/availability", headers={"Authorization": f"Bearer {token}"}, params={"starts_at": start.isoformat(), "ends_at": (start + timedelta(hours=1)).isoformat()})
    assert availability.status_code == 200 and availability.json()["available"] is False
    overlap = client.post("/api/events", headers={"Authorization": f"Bearer {token}"}, json={"title": "Overlap", "venue_id": venue["id"], "starts_at": start.isoformat(), "ends_at": (start + timedelta(hours=1)).isoformat(), "capacity": 1, "status": "PUBLISHED"})
    assert overlap.status_code == 409

def test_event_update_cancel_and_registration_listing(client, db_session):
    admin = _admin(db_session); token = client.post("/api/auth/login", json={"email": admin.email, "password": "AdminPass123!"}).json()["access_token"]
    event = _event(client, token, _venue(client, token)["id"]); user, _ = _register(client); user_headers = {"Authorization": f"Bearer {user['access_token']}"}
    assert client.patch(f"/api/events/{event['id']}", headers={"Authorization": f"Bearer {token}"}, json={"title": "Updated"}).status_code == 200
    assert client.post(f"/api/events/{event['id']}/register", headers=user_headers).status_code == 201
    assert client.get(f"/api/events/{event['id']}/registrations", headers={"Authorization": f"Bearer {token}"}).status_code == 200
    assert client.post(f"/api/events/{event['id']}/cancel", headers={"Authorization": f"Bearer {token}"}).status_code == 200
    assert client.post(f"/api/events/{event['id']}/register", headers=user_headers).status_code == 409

def test_transaction_rollback_isolation(client):
    _, email = _register(client)
    assert client.post("/api/auth/login", json={"email": email, "password": "WrongPass123!"}).status_code == 401

def _run_concurrent(workers, timeout=15):
    with ThreadPoolExecutor(max_workers=len(workers), thread_name_prefix="pg-concurrency") as pool:
        futures = [pool.submit(worker) for worker in workers]
        try:
            return [future.result(timeout=timeout) for future in futures]
        except FutureTimeoutError as exc:
            for future in futures: future.cancel()
            raise AssertionError(f"concurrency test exceeded {timeout}s timeout") from exc

def test_concurrent_last_seat_registration():
    """Two independent sessions compete for one remaining seat."""
    setup = Session(test_engine)
    admin = User(email=f"race-admin-{uuid4().hex}@example.com", password_hash=hash_password("AdminPass123!"), role=UserRole.ADMIN)
    venue = Venue(name=f"Concurrency Venue {uuid4().hex}", capacity=20, location="Test")
    user_a = User(email=f"race-a-{uuid4().hex}@example.com", password_hash=hash_password("ValidPass123!"), role=UserRole.USER)
    user_b = User(email=f"race-b-{uuid4().hex}@example.com", password_hash=hash_password("ValidPass123!"), role=UserRole.USER)
    existing = User(email=f"race-existing-{uuid4().hex}@example.com", password_hash=hash_password("ValidPass123!"), role=UserRole.USER)
    setup.add_all([admin, venue, user_a, user_b, existing]); setup.flush()
    start = datetime.now(timezone.utc) + timedelta(days=3)
    event = Event(created_by=admin.id, venue=venue, title=f"Race Event {uuid4().hex}", starts_at=start, ends_at=start + timedelta(hours=2), capacity=2, status=EventStatus.PUBLISHED)
    setup.add(event); setup.flush(); setup.add(Registration(event_id=event.id, user_id=existing.id))
    event_id = event.id
    user_ids = [user_a.id, user_b.id]
    cleanup_user_ids = [user_a.id, user_b.id, existing.id, admin.id]
    venue_id = venue.id
    setup.commit(); setup.close()
    barrier = Barrier(2)
    def attempt(user_id):
        connection = test_engine.connect(); session = Session(bind=connection, expire_on_commit=False)
        try:
            barrier.wait(timeout=10)
            user = session.get(User, user_id)
            registration_service.register(session, event_id, user)
            return 201
        except BrokenBarrierError:
            return 599
        except Exception as exc:
            return getattr(exc, "status_code", 500)
        finally:
            session.rollback(); session.close(); connection.close()
    try:
        results = _run_concurrent([lambda uid=uid: attempt(uid) for uid in user_ids])
        assert sorted(results) == [201, 409], results
        with test_engine.connect() as connection:
            count = connection.execute(select(func.count()).select_from(Registration).where(Registration.event_id == event_id, Registration.status == RegistrationStatus.ACTIVE)).scalar_one()
            assert count == 2
    finally:
        with Session(test_engine) as cleanup:
            cleanup.execute(delete(Registration).where(Registration.event_id == event_id)); cleanup.execute(delete(Event).where(Event.id == event_id)); cleanup.execute(delete(User).where(User.id.in_(cleanup_user_ids))); cleanup.execute(delete(Venue).where(Venue.id == venue_id)); cleanup.commit()

def test_concurrent_overlapping_venue_booking():
    """Two independent admin sessions compete for the same venue/time slot."""
    setup = Session(test_engine)
    admin = User(email=f"venue-race-admin-{uuid4().hex}@example.com", password_hash=hash_password("AdminPass123!"), role=UserRole.ADMIN)
    venue = Venue(name=f"Venue Race {uuid4().hex}", capacity=50, location="Test")
    setup.add_all([admin, venue]); setup.commit(); venue_id, admin_id = venue.id, admin.id; setup.close()
    start = datetime.now(timezone.utc) + timedelta(days=4)
    barrier = Barrier(2)
    def attempt(label):
        connection = test_engine.connect(); session = Session(bind=connection, expire_on_commit=False)
        try:
            barrier.wait(timeout=10)
            payload = EventCreate(title=f"Concurrent {label} {uuid4().hex}", venue_id=venue_id, starts_at=start, ends_at=start + timedelta(hours=2), capacity=10, status=EventStatus.PUBLISHED)
            event_service.create(session, payload, admin_id)
            return 201
        except BrokenBarrierError:
            return 599
        except Exception as exc:
            return getattr(exc, "status_code", 500)
        finally:
            session.rollback(); session.close(); connection.close()
    try:
        results = _run_concurrent([lambda: attempt("a"), lambda: attempt("b")])
        assert sorted(results) == [201, 409], results
        with test_engine.connect() as connection:
            count = connection.execute(select(func.count()).select_from(Event).where(Event.venue_id == venue_id, Event.status.in_([EventStatus.DRAFT, EventStatus.PUBLISHED]), Event.starts_at < start + timedelta(hours=2), Event.ends_at > start)).scalar_one()
            assert count == 1
    finally:
        with Session(test_engine) as cleanup:
            cleanup.execute(delete(Event).where(Event.venue_id == venue_id)); cleanup.execute(delete(User).where(User.id == admin_id)); cleanup.execute(delete(Venue).where(Venue.id == venue_id)); cleanup.commit()
