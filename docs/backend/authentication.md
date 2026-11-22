# Authentication

Registration hashes passwords with Argon2id through `pwdlib`. Login returns a short-lived JWT signed with `JWT_SECRET_KEY`; the token includes only user ID, role and expiry. `get_current_user` reloads the user from PostgreSQL and checks active status. Roles are `ADMIN` and `USER`; role changes are not exposed through self-service profile updates.

