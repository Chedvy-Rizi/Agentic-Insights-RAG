# Task Management System — Architecture Decision Records

> This file captures the *why* behind significant technical choices. Each entry
> is written after a decision is made and is intended to survive long after the
> person who made the decision has moved on. Future engineers deserve context,
> not just conclusions.

---

## ADR-001 — JWT over Session-Based Authentication

**Date:** 2024-01-15
**Status:** Accepted

### Context

We needed to choose an authentication mechanism for the API. The two primary
candidates were server-side sessions (stored in Redis or PostgreSQL) and
stateless JWTs (JSON Web Tokens).

### Decision

We use **JWTs with a dual-token strategy**: a short-lived Access Token and a
long-lived Refresh Token.

- **Access Token:** Signed with `HS256`, expires in **15 minutes**, sent in
  the `Authorization` header on every request.
- **Refresh Token:** Expires in **7 days**, stored in an `HttpOnly`, `Secure`,
  `SameSite=Strict` cookie. Used only to silently obtain a new Access Token.

### Rationale

| Concern                   | Sessions                          | JWT (chosen)                            |
|---------------------------|-----------------------------------|-----------------------------------------|
| Horizontal scaling        | Requires shared session store     | Stateless — any server can verify       |
| Logout / revocation       | Trivial (delete session)          | Requires token denylist (see trade-off) |
| Implementation complexity | Low                               | Medium                                  |
| Infrastructure dependency | Redis or DB session table         | None beyond the secret key              |

The system is expected to run across multiple server instances behind a load
balancer. Stateless JWT verification eliminates the need for a shared session
store, which would be a single point of failure and an infrastructure cost.

### Trade-offs Accepted

The main weakness of JWTs is that Access Tokens cannot be instantly revoked.
If a token is stolen, it remains valid until it expires. We mitigate this with:

1. A **15-minute expiry** — the attack window is small.
2. A **token denylist** in Redis for explicit logout and password-change events.
   This adds a fast read-only lookup on every request, which is acceptable.
3. Refresh Tokens are stored `HttpOnly` — they are invisible to JavaScript,
   making XSS attacks unable to steal them.

---

## ADR-002 — PostgreSQL over a NoSQL Alternative

**Date:** 2024-01-18
**Status:** Accepted

### Context

Task data is hierarchical (projects → tasks → subtasks → comments → attachments)
and heavily relational (users assigned to tasks, members of projects, labels
shared across tasks). We evaluated PostgreSQL and MongoDB.

### Decision

**PostgreSQL**, managed via Prisma ORM.

### Rationale

The data model has clear, stable relationships and benefits directly from
foreign key constraints, cascading deletes, and JOIN performance. MongoDB's
flexible schema is valuable when data shape is unknown or varies wildly between
records — that is not the case here.

PostgreSQL's `jsonb` column type gives us a safety valve for genuinely flexible
data (custom task fields, integration metadata) without abandoning a relational
foundation.

Prisma was chosen as the ORM because it generates a TypeScript client from the
schema, eliminating an entire class of type-mismatch bugs between the database
and the application layer. Migrations are version-controlled and reproducible.

### Trade-offs Accepted

PostgreSQL requires more operational care than a managed NoSQL service.
We accept this because the team has PostgreSQL experience, and managed offerings
(e.g., Railway, Supabase, RDS) reduce the operational burden significantly.

---

## ADR-003 — RTL-First Component Architecture for Hebrew Support

**Date:** 2024-01-22
**Status:** Accepted

### Context

The product is used in Israel. Hebrew is a required language, not a future
consideration. We needed to decide how to implement RTL layout support.

### Decision

All component stylesheets use **CSS Logical Properties** exclusively. Direction
is set once on `<html dir="...">` by the i18n provider. There is no separate
RTL stylesheet, no mirrored component tree, and no `rtl:` CSS class prefix.

### Rationale

We evaluated three approaches:

**Option A — Duplicate stylesheets:** Maintain an `.rtl.css` file alongside
each component. Rejected: this doubles the maintenance burden and creates
inevitable drift between the two files.

**Option B — Tailwind `rtl:` variants:** Use Tailwind's directional variant
prefix. Rejected: it requires every physical property to be explicitly paired
with an RTL override. Easy to forget; hard to audit.

**Option C — CSS Logical Properties (chosen):** Write `margin-inline-start`
instead of `margin-left`. The browser automatically interprets "start" as
"left" in LTR and "right" in RTL. One stylesheet. No duplication. Direction
is managed entirely by the `dir` attribute on `<html>`.

This approach requires discipline from every contributor — old habits lead to
writing `margin-left` — but we enforce it with an ESLint plugin
(`eslint-plugin-logical-properties`) that flags physical directional CSS.

### Trade-offs Accepted

Browser support for CSS Logical Properties is now excellent (all modern
browsers). IE11 is explicitly out of scope. The ESLint rule catches violations
at development time before they reach review.

---

## ADR-004 — Zustand over Redux for Client State

**Date:** 2024-01-25
**Status:** Accepted

### Context

The application needs shared client state: the authenticated user, active
workspace, UI preferences (language, theme), and notification queue. We
evaluated Redux Toolkit and Zustand.

### Decision

**Zustand** for all shared client state. React Query handles all server state.

### Rationale

Redux Toolkit is an excellent choice for very large teams where the strict
action/reducer/selector pattern provides governance. For a product at this
scale, the boilerplate-to-value ratio tilts unfavorably.

Zustand stores are plain TypeScript objects with actions co-located in the
same file. They are trivially testable (no Provider wrapping needed in tests),
have zero setup beyond the store definition, and integrate naturally with React
DevTools via a middleware.

The critical architectural decision is the **separation of concerns**:
Zustand owns only local application state (UI, preferences, auth user object).
It does not own or cache server data. That responsibility belongs entirely to
React Query, which has purpose-built infrastructure for caching, invalidation,
background refetching, and error states.

### Trade-offs Accepted

Zustand's flexibility means discipline must come from convention rather than
framework enforcement. We document this separation of concerns here and in
`architecture.md` to ensure new contributors understand the contract.

---

## ADR-005 — Vite over Create React App

**Date:** 2024-01-25
**Status:** Accepted

### Context

We needed a build toolchain for the React frontend. The legacy choice would be
Create React App. Vite is the current community standard.

### Decision

**Vite** with the `@vitejs/plugin-react` plugin and TypeScript.

### Rationale

Create React App is effectively unmaintained as of 2024 and produces slow
development builds via Webpack. Vite uses native ES modules in development
(near-instant server start regardless of project size) and Rollup for
production builds (well-optimized output with good tree-shaking).

The migration risk is negligible for a new project — there is nothing to
migrate from.