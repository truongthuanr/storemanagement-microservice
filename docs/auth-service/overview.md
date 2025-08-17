# Auth Service - Overview

## 1. Purpose
The **Auth Service** is responsible for handling authentication and authorization across the system.  
It ensures that only verified users can access protected resources, and that user actions are restricted based on their roles and permissions.

This service acts as the **gateway for identity management**, providing tokens that can be verified by other services.

---

## 2. Scope
### In Scope (Phase 1 - MVP)
- **User signup** with email/username + password.
- **User login** and credential verification.
- **JWT issuance** (access token + refresh token).
- **Token verification** (middleware/interceptor).
- **Refresh token flow**.
- **Basic role-based authorization** (e.g., `user`, `admin`).
- **Logout** (revoke refresh tokens).

### Out of Scope (Future Phase)
- Social login (Google, Facebook, Apple).
- Multi-Factor Authentication (MFA, OTP).
- Password reset via email/SMS.
- Fine-grained permission system (ABAC).
- Session management dashboard for admins.

---

## 3. Consumers
Services that rely on Auth Service:
- **User Service** – uses Auth for identity linkage.
- **Order Service** – verifies token before creating or fetching orders.
- **Inventory Service** – ensures only admin/merchant can update stock.
- **Payment Service** – ensures only authorized users can perform transactions.
- **Notification Service** – may subscribe to Auth events (login, account locked).

---

## 4. Non-Functional Requirements
- **Security**: Passwords hashed with bcrypt/argon2; TLS enforced.
- **Performance**: Token validation must be lightweight (< 50ms).
- **Scalability**: Stateless JWT verification allows horizontal scaling.
- **Reliability**: Token revocation supported via refresh token blacklist.
- **Observability**: Logging, metrics, and audit trails for login attempts.

---

## 5. High-Level Architecture
- REST API (FastAPI).
- Database (PostgreSQL/MySQL) for credentials and refresh tokens.
- JWT signing with HS256/RS256.
- Optional integration with Kafka for publishing security-related events.

---

## 6. Example Events
- `auth.user_created`
- `auth.login.success`
- `auth.login.failed`
- `auth.user_locked`
