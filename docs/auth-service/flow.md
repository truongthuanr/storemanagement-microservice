# Auth Service - Flows

## 1. Signup Flow
User registers with email + password.  
Auth creates credentials and publishes event `auth.user_created`.

```mermaid
sequenceDiagram
    participant Client
    participant Auth
    participant AuthDB
    participant Kafka

    Client ->> Auth: POST /auth/signup (email, password)
    Auth ->> AuthDB: Insert user credentials
    AuthDB -->> Auth: OK
    Auth ->> Kafka: Publish event "auth.user_created"
    Auth -->> Client: 201 Created (user_id, email, role)
```

---

## 2. Login Flow
User provides credentials → Auth validates → returns JWT (access + refresh token).

```mermaid
sequenceDiagram
    participant Client
    participant Auth
    participant AuthDB

    Client ->> Auth: POST /auth/login (email, password)
    Auth ->> AuthDB: Verify credentials
    AuthDB -->> Auth: Success
    Auth ->> AuthDB: Insert refresh_token
    Auth -->> Client: 200 OK (access_token + refresh_token)
```

---

## 3. Refresh Token Flow
Client exchanges refresh token for a new access token.

```mermaid
sequenceDiagram
    participant Client
    participant Auth
    participant AuthDB

    Client ->> Auth: POST /auth/refresh (refresh_token)
    Auth ->> AuthDB: Validate refresh_token (not expired, not revoked)
    AuthDB -->> Auth: Valid
    Auth ->> AuthDB: Update refresh_token (rotate or extend expiry)
    Auth -->> Client: 200 OK (new access_token)
```

---

## 4. Logout Flow
Client revokes a refresh token (logout from one session).

```mermaid
sequenceDiagram
    participant Client
    participant Auth
    participant AuthDB

    Client ->> Auth: POST /auth/logout (refresh_token)
    Auth ->> AuthDB: Mark refresh_token as revoked
    AuthDB -->> Auth: OK
    Auth -->> Client: 200 OK (message: "Logged out successfully")
```

---

## 5. Me (Get Current User)
Client uses access token to retrieve user identity from JWT (no DB call).

```mermaid
sequenceDiagram
    participant Client
    participant OrderService
    participant Auth (JWT Verify)

    Client ->> OrderService: GET /orders (Authorization: Bearer <JWT>)
    OrderService ->> Auth: Verify JWT signature
    Auth -->> OrderService: Token valid (user_id, role)
    OrderService -->> Client: 200 OK (user data or orders)
```

---

## Notes
- **Signup** may trigger `User Service` (via event) to create an empty profile.
- **JWT verification** should be stateless (using shared secret or public/private key).
- **Refresh token** allows long-lived sessions without keeping access token forever.
