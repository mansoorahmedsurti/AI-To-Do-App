# Phase II Plan: Monorepo & Auth

## 1. Project Restructuring
* Create `/frontend` (Next.js) and `/backend` (FastAPI) folders.
* Create root `docker-compose.yml` for local Postgres (User: postgres, DB: todos).

## 2. Backend Implementation (PostgreSQL + FastAPI + SQLModel)
* Set up PostgreSQL connection with Docker Compose
* Create User and Todo models using SQLModel
* Implement API endpoints with proper authentication
* Remove all JSON file usage (comply with constitution)

## 3. Frontend Implementation (Next.js 15 + Better Auth)
* Initialize Next.js 15 project with Tailwind and Shadcn
* Integrate Better Auth for user authentication
* Create UI components for todo management
* Connect frontend to backend API