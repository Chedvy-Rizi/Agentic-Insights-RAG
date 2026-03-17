# Task Management System - Technical Decisions and Rationale

## Overview

This document outlines the key technical decisions made during the design and development of the Task Management System. Each decision includes the rationale, alternatives considered, and implementation details.

---

## Decision 1: Authentication Strategy - JWT (JSON Web Tokens)

### Status: **APPROVED** ✓

### Date: March 2026

### Participants
- Backend Team Lead
- Security Officer
- Frontend Lead

### Decision
Implement JWT (JSON Web Tokens) as the authentication mechanism for the Task Management System.

### Rationale

#### 1. Stateless Authentication
- No server-side session storage required
- Reduces database load for authentication checks
- Allows horizontal scaling without session synchronization
- Supports microservices architecture

#### 2. Cross-Domain and CORS Support
- Ideal for REST APIs and modern web applications
- Works seamlessly with CORS
- Supports multiple frontend deployments
- Enables API gateway patterns

#### 3. Mobile and SPA-Friendly
- Native support for Single Page Applications (React)
- Works efficiently with mobile applications
- No session cookie restrictions
- Token stored in secure storage (localStorage or secure cookie)

#### 4. Industry Standard
- Widely adopted and well-supported
- Extensive library ecosystem
- Well-documented security best practices
- Strong community support

### Alternatives Considered

#### 1. Session-Based Authentication
- **Pros**: Traditional, simple implementation
- **Cons**: Requires server-side storage, harder to scale horizontally, issues with CORS
- **Decision**: Rejected due to scalability concerns

#### 2. OAuth 2.0
- **Pros**: Industry standard for third-party integrations
- **Cons**: Overkill for current requirements, adds complexity
- **Decision**: Deferred for future phases if third-party integrations needed

#### 3. API Keys
- **Pros**: Simple for service-to-service communication
- **Cons**: Weak authentication for user-centric applications
- **Decision**: Not suitable for user authentication

### Implementation Details

#### JWT Token Structure
```javascript
// Header
{
  "alg": "HS256",
  "typ": "JWT"
}

// Payload
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "user_role": "user",
  "iat": 1710518400,
  "exp": 1710604800,  // 24 hours expiration
  "iss": "task-management-system",
  "aud": "task-management-app"
}

// Signature
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

#### Token Management
- **Access Token**: 24-hour expiration
- **Refresh Token**: 7-day expiration, stored in secure HTTP-only cookie
- **Token Refresh Endpoint**: `/api/auth/refresh-token`
- **Logout**: Token blacklist in Redis (optional)

#### Security Measures
```javascript
// Token generation with HS256
const token = jwt.sign(
  {
    sub: userId,
    email: user.email,
    user_role: user.user_role
  },
  process.env.JWT_SECRET,
  {
    algorithm: 'HS256',
    expiresIn: '24h',
    issuer: 'task-management-system'
  }
);

// Token verification
jwt.verify(token, process.env.JWT_SECRET, {
  algorithms: ['HS256'],
  issuer: 'task-management-system'
});
```

#### Frontend Implementation
```javascript
// Store token securely
localStorage.setItem('accessToken', token);

// Include in API requests
fetch('/api/tasks', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

// Refresh token automatically before expiration
const refreshTokens = async () => {
  const response = await fetch('/api/auth/refresh-token', {
    method: 'POST',
    credentials: 'include'
  });
  const { accessToken } = await response.json();
  localStorage.setItem('accessToken', accessToken);
};
```

#### Backend Middleware
```javascript
// Express middleware for JWT validation
const authMiddleware = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = decoded;
    next();
  });
};

// Apply to protected routes
app.get('/api/tasks', authMiddleware, taskController.getTasks);
```

---

## Decision 2: Database Schema - Enhanced User Table Fields

### Status: **APPROVED** ✓

### Date: March 2026

### Participants
- Database Architect
- Backend Team Lead
- Product Manager

### Decision
Add `last_login` and `user_role` fields to the user table in PostgreSQL.

### Rationale

#### 1. `last_login` Field (TIMESTAMP)

**Purpose**: Track user engagement and account activity

**Benefits**:
- Identify inactive accounts for automatic disabling
- Detect suspicious login patterns
- Generate user engagement analytics
- Support account recovery (detect unauthorized access)
- Improve security monitoring

**Use Cases**:
```sql
-- Find inactive users (no login for 90 days)
SELECT id, email, last_login
FROM users
WHERE last_login < NOW() - INTERVAL '90 days';

-- Account activity audit
SELECT email, last_login
FROM users
ORDER BY last_login DESC;

-- Detect unusual login patterns
SELECT email, last_login, created_at
FROM users
WHERE last_login > created_at + INTERVAL '1 day'
AND last_login < created_at + INTERVAL '2 days';
```

#### 2. `user_role` Field (ENUM)

**Purpose**: Support role-based access control (RBAC)

**Role Definitions**:
- **admin**: Full system access, user management, system settings
- **manager**: Assign tasks, view team progress, manage projects
- **user**: Create and manage own tasks, view assigned tasks

**Benefits**:
- Fine-grained authorization control
- Scalable permission model
- Support team structures
- Audit trail for role-based actions
- Enable delegation of administrative tasks

**Implementation**:
```sql
-- Create ENUM type
CREATE TYPE user_role_enum AS ENUM ('admin', 'manager', 'user');

-- Add to users table
ALTER TABLE users ADD COLUMN user_role user_role_enum DEFAULT 'user';

-- Index for performance
CREATE INDEX idx_users_role ON users(user_role);
```

### Schema Changes

#### Original User Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Enhanced User Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  user_role user_role_enum DEFAULT 'user' NOT NULL,
  last_login TIMESTAMP,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(user_role);
CREATE INDEX idx_users_last_login ON users(last_login);
CREATE INDEX idx_users_is_active ON users(is_active);
```

### Alternatives Considered

#### 1. Separate Permissions Table
```sql
CREATE TABLE permissions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  permission_code VARCHAR(50),
  granted_at TIMESTAMP
);
```
- **Pros**: Highly flexible, granular permissions
- **Cons**: More complex queries, performance overhead
- **Decision**: Deferred for future enhancement

#### 2. Role Hierarchy with Groups
- **Pros**: Complex organizational structures
- **Cons**: Unnecessary complexity for current scope
- **Decision**: Simple enum sufficient for v1

### Implementation Strategy

#### User Service Update
```javascript
// Update last_login on successful authentication
const updateLastLogin = async (userId) => {
  await db.query(
    'UPDATE users SET last_login = NOW() WHERE id = $1',
    [userId]
  );
};

// Get user with role for JWT
const getUserById = async (userId) => {
  const result = await db.query(
    'SELECT id, email, user_role FROM users WHERE id = $1',
    [userId]
  );
  return result.rows[0];
};

// Check user role for authorization
const hasRole = (req, requiredRoles) => {
  return requiredRoles.includes(req.user.user_role);
};
```

#### Role-Based Middleware
```javascript
// Middleware for role-based access control
const requireRole = (...roles) => {
  return (req, res, next) => {
    if (!hasRole(req, roles)) {
      return res.status(403).json({ 
        error: 'Insufficient permissions' 
      });
    }
    next();
  };
};

// Usage in routes
app.post('/api/users', 
  authMiddleware,
  requireRole('admin'),
  userController.createUser
);

app.patch('/api/tasks/:id/assign',
  authMiddleware,
  requireRole('admin', 'manager'),
  taskController.assignTask
);
```

#### Migration Script
```sql
-- Migration file: migrations/002_add_user_role_and_last_login.sql

BEGIN;

-- Create ENUM type
CREATE TYPE user_role_enum AS ENUM ('admin', 'manager', 'user');

-- Add columns to existing table
ALTER TABLE users
ADD COLUMN user_role user_role_enum DEFAULT 'user' NOT NULL,
ADD COLUMN last_login TIMESTAMP;

-- Create indexes
CREATE INDEX idx_users_role ON users(user_role);
CREATE INDEX idx_users_last_login ON users(last_login);

-- Set initial admin (first user as admin)
UPDATE users SET user_role = 'admin' 
WHERE id = (SELECT id FROM users ORDER BY created_at ASC LIMIT 1);

COMMIT;
```

---

## Decision 3: Technology Stack Selection

### Status: **APPROVED** ✓

### Date: March 2026

### Participants
- Tech Lead
- DevOps Engineer
- Frontend Lead
- Backend Lead

### Decision
Use PostgreSQL for database, Node.js/Express for backend, and React for frontend.

### Rationale

#### PostgreSQL Selection
1. **ACID Compliance**: Data consistency and reliability
2. **JSON Support**: JSONB for flexible data structures
3. **Full-Text Search**: Enhanced search capabilities
4. **Scalability**: Proven in production environments
5. **Cost**: Open-source, no licensing fees

#### Node.js/Express Selection
1. **JavaScript Unification**: Single language across stack
2. **Async/Await**: Modern, clean async code
3. **Package Ecosystem**: npm provides extensive libraries
4. **Performance**: Event-driven, non-blocking I/O
5. **Community**: Large, active development community

#### React Selection
1. **Component Reusability**: Build with modular components
2. **Performance**: Virtual DOM and efficient rendering
3. **Developer Experience**: Hot reloading, great tooling
4. **RTL Support**: Community packages for Right-to-Left
5. **Career Prospect**: Market-leading framework

### Rejected Alternatives

| Stack | Reason |
|-------|--------|
| Django/Python | Overkill for current scope, slower for real-time needs |
| .NET/C# | Licensing concerns, larger deployment footprint |
| Vue.js | Less mature ecosystem for enterprise use |
| Angular | Steeper learning curve, more boilerplate |

---

## Decision 4: RTL (Right-to-Left) Support Implementation

### Status: **APPROVED** ✓

### Date: March 2026

### Participants
- UX Designer
- Frontend Lead
- Product Manager (Hebrew Market)

### Decision
Implement comprehensive RTL support for Hebrew language using CSS logical properties and React component design patterns.

### Rationale

#### Market Demand
- Target Hebrew-speaking user base
- Regional competitive advantage
- Natural language support requirement

#### Technical Approach
- **CSS Logical Properties**: Use `margin-inline`, `padding-block` instead of directional properties
- **Direction Attribute**: Set `dir="rtl"` on HTML root and components
- **Flex Direction**: Reverse flex layouts for RTL context
- **Text Alignment**: Conditional alignment based on language

#### Implementation Priority
1. **Phase 1**: Core UI components (navigation, buttons, forms)
2. **Phase 2**: Task management interface
3. **Phase 3**: Dashboard and analytics

### Testing Requirements
- Hebrew language content rendering
- Number and date format localization
- Icon and image directionality
- Component interaction in RTL mode

---

## Decision 5: Color Scheme - Navy Blue Primary (#001f3f)

### Status: **APPROVED** ✓

### Date: March 2026

### Rationale

#### Accessibility
- High contrast ratio with white text (21:1)
- Complies with WCAG AAA standards
- Distinguishable by colorblind users

#### Professionalism
- Corporate and trustworthy appearance
- Suitable for task management application
- Industry-standard for productivity tools

#### Visual Hierarchy
- Distinguished primary actions
- Clear visual distinction from secondary elements
- Maintains visual consistency throughout interface

---

## Future Decisions (Pending)

### 1. Caching Strategy
- Consideration: Redis for session and query caching
- Status: Under evaluation

### 2. Real-Time Collaboration
- Consideration: WebSocket integration for live updates
- Status: Planned for v2

### 3. File Attachments
- Consideration: S3 or local storage for task attachments
- Status: Planned for v2

### 4. Internationalization (i18n)
- Consideration: i18next library for multilingual support
- Status: Planned for v2

### 5. OAuth Integration
- Consideration: Google/GitHub login for user convenience
- Status: Planned for v2

---

## Change Log

| Date | Decision | Change | Reason |
|------|----------|--------|--------|
| 2026-03-15 | JWT Auth | Approved | Initial setup |
| 2026-03-15 | Database Schema | Approved | User role and login tracking |
| 2026-03-15 | Tech Stack | Approved | Initial architecture |
| 2026-03-15 | RTL Support | Approved | Hebrew market support |
| 2026-03-15 | Color Scheme | Approved | Brand consistency |

