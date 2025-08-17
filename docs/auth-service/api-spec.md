# Auth Service - API Specification

## Base URL
```
/auth
```

---

## 1. Signup
### Endpoint
`POST /auth/signup`

### Description
Register a new user account (email/username + password).  
Emits event `auth.user_created`.

### Request
```json
{
  "email": "user@example.com",
  "password": "secret123",
  "role": "user"
}
```

### Response (201 Created)
```json
{
  "user_id": "uuid-1234-5678",
  "email": "user@example.com",
  "role": "user",
  "created_at": "2025-08-17T12:00:00Z"
}
```

---

## 2. Login
### Endpoint
`POST /auth/login`

### Description
Authenticate user credentials and issue tokens.

### Request
```json
{
  "email": "user@example.com",
  "password": "secret123"
}
```

### Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "dGhpc19pc19hX3JlZnJlc2hfdG9rZW4",
  "token_type": "Bearer",
  "expires_in": 900
}
```

---

## 3. Refresh Token
### Endpoint
`POST /auth/refresh`

### Description
Exchange a valid refresh token for a new access token.

### Request
```json
{
  "refresh_token": "dGhpc19pc19hX3JlZnJlc2hfdG9rZW4"
}
```

### Response (200 OK)
```json
{
  "access_token": "new.jwt.token",
  "token_type": "Bearer",
  "expires_in": 900
}
```

---

## 4. Logout
### Endpoint
`POST /auth/logout`

### Description
Revoke a refresh token (logout the session).

### Request
```json
{
  "refresh_token": "dGhpc19pc19hX3JlZnJlc2hfdG9rZW4"
}
```

### Response (200 OK)
```json
{ "message": "Logged out successfully" }
```

---

## 5. Me (Get Current User)
### Endpoint
`GET /auth/me`

### Description
Return user information based on JWT (access token).  
Requires `Authorization: Bearer <access_token>`.

### Response (200 OK)
```json
{
  "user_id": "uuid-1234-5678",
  "email": "user@example.com",
  "role": "user",
  "exp": 1692193929
}
```

---

## 6. Token Introspection (Optional)
### Endpoint
`POST /auth/introspect`

### Description
Validate a token and return its metadata. Useful for other services if they cannot verify JWT locally.

### Request
```json
{
  "token": "eyJhbGciOi..."
}
```

### Response (200 OK)
```json
{
  "active": true,
  "user_id": "uuid-1234-5678",
  "role": "user",
  "exp": 1692193929
}
```
