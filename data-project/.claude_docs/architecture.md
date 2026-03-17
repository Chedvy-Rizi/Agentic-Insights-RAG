# Task Management System — Architecture Overview

> This document describes the structural backbone of the system: how data flows,
> where responsibilities live, and why the pieces are arranged the way they are.
> It is intended to be a living reference, not a frozen blueprint.

---

## The Big Picture

The system is split into two clearly separated worlds: a **React frontend** that
owns everything the user sees and touches, and a **Node.js/Express backend** that
owns all data, business logic, and security enforcement. They speak exclusively
through a versioned REST API (`/api/v1/...`), making each side independently
deployable and testable.
```
┌─────────────────────┐         HTTPS / REST          ┌──────────────────────┐
│                     │  ──────────────────────────►  │                      │
│   React Client      │                               │   Express API Server │
│   (Vite + TS)       │  ◄──────────────────────────  │   (Node.js + TS)     │
│                     │        JSON responses          │                      │
└─────────────────────┘                               └──────────┬───────────┘
                                                                  │
                                                    ┌─────────────▼────────────┐
                                                    │                          │
                                                    │   PostgreSQL Database    │
                                                    │   (via Prisma ORM)       │
                                                    │                          │
                                                    └──────────────────────────┘
```

---

## Frontend Layer — React

The client is a **Single Page Application** built with Vite and TypeScript.
Component state that affects only one screen lives locally (useState/useReducer).
State that needs to be shared across routes — authenticated user, active workspace,
notification queue — lives in **Zustand** stores, chosen for its minimal boilerplate
and easy devtools integration.

All server data fetching goes through **React Query (TanStack Query)**, which
handles caching, background refetch, loading states, and optimistic updates. This
means the UI never talks to `fetch()` directly.

**Directory layout (abbreviated):**
```
src/
├── api/          # Typed API client functions (axios instances, query hooks)
├── components/   # Shared, stateless UI primitives
├── features/     # Feature-sliced modules (tasks, auth, projects, users)
│   └── tasks/
│       ├── components/
│       ├── hooks/
│       └── store.ts
├── layouts/      # App shell, sidebar, header
├── pages/        # Route-level components (thin wrappers)
├── i18n/         # Translation files (he.json, en.json) + RTL config
└── styles/       # Global tokens, CSS variables, direction utilities
```

---

## Backend Layer — Express + Node.js

The API server follows a **layered architecture**: routes → controllers →
services → repositories → database. Each layer has a single job:

| Layer          | Responsibility                                        |
|----------------|-------------------------------------------------------|
| **Routes**     | Declare HTTP verbs and paths. Apply middleware.       |
| **Controllers**| Parse request, call services, format response.        |
| **Services**   | Enforce business rules. Orchestrate multiple repos.   |
| **Repositories**| Prisma queries only. No business logic here.         |
| **Middleware** | Auth (JWT), validation (Zod), error handling, logging.|

This separation means business logic can be unit-tested without spinning up a
server, and database queries can be swapped without touching service code.

---

## Database Layer — PostgreSQL

PostgreSQL was selected for its reliability with relational, hierarchical data
(projects → tasks → subtasks → comments) and its excellent support for
`jsonb` columns where task metadata needs to be flexible.

Schema management is handled entirely through **Prisma Migrate**, which keeps
the schema file as the single source of truth and generates type-safe query
clients for TypeScript.

**Core entities:**
```
Users ──< ProjectMembers >── Projects
                                │
                               Tasks
                                ├── Subtasks
                                ├── Assignees (Users)
                                ├── Labels
                                └── Comments (Users)
```

Indexes exist on `tasks.project_id`, `tasks.assignee_id`, `tasks.status`,
and `tasks.due_date` — the four most common filter/sort axes.

---

## Authentication Flow

JWT-based stateless authentication. Details and rationale are documented
separately in `decisions.md`. The short version:

1. Client sends credentials → server issues **Access Token** (15 min) +
   **Refresh Token** (7 days, stored in an `HttpOnly` cookie).
2. Every subsequent request carries the Access Token in the
   `Authorization: Bearer <token>` header.
3. When the Access Token expires, the client's Axios interceptor silently
   calls `/api/v1/auth/refresh` and retries the original request.
4. The Express `authenticate` middleware verifies every protected route.
   No session store. No server state.

---

## RTL & Internationalization

The UI supports Hebrew (RTL) and English (LTR) without maintaining two
component trees. See `ui-rules.md` for the complete implementation contract.
The short version: direction is set at `<html dir="...">`, all spacing and
positioning uses logical CSS properties (`margin-inline-start` instead of
`margin-left`), and icons that carry directional meaning are flipped via
`[dir="rtl"] .icon-directional { transform: scaleX(-1); }`.

---

## Environment Configuration

| Variable              | Purpose                              |
|-----------------------|--------------------------------------|
| `DATABASE_URL`        | PostgreSQL connection string         |
| `JWT_ACCESS_SECRET`   | Signing key for Access Tokens        |
| `JWT_REFRESH_SECRET`  | Signing key for Refresh Tokens       |
| `CLIENT_ORIGIN`       | CORS allowed origin                  |
| `NODE_ENV`            | `development` / `production` / `test`|

Secrets are never committed. A `.env.example` file documents every variable
without values.