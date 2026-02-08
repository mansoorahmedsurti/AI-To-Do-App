# Phase II Constitution: The Web Era

## 1. Mandatory Tech Stack
* **Auth:** Better Auth (Frontend) -> Issues JWT -> Verified by Backend.
* **Database:** PostgreSQL ONLY (Docker locally, Neon in prod). NO SQLite.
* **Backend:** FastAPI + SQLModel.
* **Frontend:** Next.js 15 + Tailwind + Shadcn.

## 2. Strict Constraints
* **NO JSON Persistence:** Data must be stored in Postgres. `todos.json` is BANNED.
* **NO Custom Auth Logic:** Do not write password hashing code. Use Better Auth.
* **Monorepo:** `/frontend` and `/backend` must be distinct.