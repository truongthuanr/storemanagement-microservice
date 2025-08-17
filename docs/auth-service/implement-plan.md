# Auth Service - Implementation Plan

## 1. Goals
Deliver a secure, minimal viable **Auth Service** to handle:
- User signup
- User login
- JWT issuance and verification
- Refresh token flow
- Logout (token revocation)
- Basic role-based authorization

---

## 2. Milestones

### Milestone 1: Project Setup
- Initialize FastAPI project structure
- Setup Poetry/pipenv/requirements.txt for dependencies
- Setup Dockerfile + docker-compose (for DB, service)
- Integrate Alembic for DB migrations
- Add base logging, config management (dotenv or pydantic-settings)

**Deliverable**: Empty FastAPI app running, DB migrations working

---

### Milestone 2: Database Layer
- Define models: `users_auth`, `refresh_tokens`
- Implement Alembic migrations
- Setup SQLAlchemy session management
- Add DB unit tests

**Deliverable**: DB schema created, tested with migrations

---

### Milestone 3: Signup Flow
- Implement `POST /auth/signup`
- Hash password with bcrypt/argon2
- Save credentials in DB
- Emit event `auth.user_created` (Kafka/RabbitMQ)
- Unit tests for signup

**Deliverable**: New users can be created securely

---

### Milestone 4: Login & JWT
- Implement `POST /auth/login`
- Verify credentials
- Issue JWT (access + refresh token)
- Save refresh token in DB
- Add PyJWT or jose for token signing
- Unit tests for login flow

**Deliverable**: Users can log in and get valid tokens

---

### Milestone 5: Token Management
- Implement `POST /auth/refresh` (rotate refresh tokens)
- Implement `POST /auth/logout` (revoke refresh token)
- Middleware for JWT validation (role extraction)
- Unit tests for token lifecycle

**Deliverable**: Secure token lifecycle with rotation and revocation

---

### Milestone 6: Me Endpoint & Role Checks
- Implement `GET /auth/me` (extract identity from JWT)
- Add basic role-based check in middleware (admin/user)
- Integration tests across flows

**Deliverable**: Other services can trust JWT claims to enforce roles

---

### Milestone 7: Security Hardening
- Rate limiting on login (Redis-based)
- Account lock after N failed attempts
- TLS/HTTPS enforcement (if behind API gateway)
- Structured logging for audit

**Deliverable**: Auth hardened against brute-force & replay attacks

---

### Milestone 8: Documentation & Deployment
- Finalize docs (API Spec, Flows, Security, Events)
- Add OpenAPI/Swagger auto-docs
- CI/CD pipeline (GitHub Actions/GitLab CI)
- Deployment to dev/staging cluster (Docker/K8s)

**Deliverable**: Auth service ready for staging & integration with other services

---

## 3. Timeline (suggested)
- **Week 1**: Milestones 1–2  
- **Week 2**: Milestones 3–4  
- **Week 3**: Milestones 5–6  
- **Week 4**: Milestones 7–8  

---

## 4. Risks
- Token rotation logic errors → risk of orphaned sessions
- Password hashing performance (bcrypt cost factor too high/low)
- Event broker downtime (Kafka/RabbitMQ) → use retry mechanism
- JWT key management (rotate safely without downtime)

---

## 5. Next Steps
1. Setup repo + project skeleton (Milestone 1)  
2. Write DB migrations (Milestone 2)  
3. Implement signup/login → end-to-end test with Postman/HTTPie  
4. Connect to Kafka/RabbitMQ for events  
5. Add integration test with User Service (subscribe `auth.user_created`)  
