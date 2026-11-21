# Frontend architecture

Next.js App Router provides pages and server/client boundaries. `services/` owns typed API calls, `lib/` owns auth/configuration, and components remain presentational. Browser state must be role-scoped and should not contain private backend secrets. The Phase 0 page is the only implemented UI; dashboard, event, registration, venue and chat pages are planned.

