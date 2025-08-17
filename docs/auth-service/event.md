# Auth Service - Events

## Overview
Auth Service emits events when critical authentication/authorization actions occur.  
Events are published to the message broker (Kafka/RabbitMQ) so other services can react asynchronously.  

---

## 1. Event: User Created
### Name
`auth.user_created`

### Description
Emitted when a new user successfully signs up.  
Other services (User Service, Notification, Loyalty) may subscribe to this event.

### Payload
```json
{
  "event": "auth.user_created",
  "timestamp": "2025-08-17T12:00:00Z",
  "correlation_id": "uuid-1234",
  "producer": "auth-service",
  "data": {
    "user_id": "uuid-5678",
    "email": "user@example.com",
    "role": "user"
  }
}
```

---

## 2. Event: Login Success
### Name
`auth.login.success`

### Description
Emitted when a user logs in successfully.  
Fraud detection or analytics services may use this.

### Payload
```json
{
  "event": "auth.login.success",
  "timestamp": "2025-08-17T12:05:00Z",
  "correlation_id": "uuid-2222",
  "producer": "auth-service",
  "data": {
    "user_id": "uuid-5678",
    "email": "user@example.com",
    "ip": "192.168.1.10",
    "user_agent": "Mozilla/5.0"
  }
}
```

---

## 3. Event: Login Failed
### Name
`auth.login.failed`

### Description
Emitted when a login attempt fails.  
Helps security monitoring and brute-force detection.

### Payload
```json
{
  "event": "auth.login.failed",
  "timestamp": "2025-08-17T12:06:00Z",
  "correlation_id": "uuid-3333",
  "producer": "auth-service",
  "data": {
    "email": "user@example.com",
    "ip": "192.168.1.11",
    "reason": "invalid_password"
  }
}
```

---

## 4. Event: User Locked
### Name
`auth.user_locked`

### Description
Emitted when a user account is locked due to repeated failed login attempts.

### Payload
```json
{
  "event": "auth.user_locked",
  "timestamp": "2025-08-17T12:10:00Z",
  "correlation_id": "uuid-4444",
  "producer": "auth-service",
  "data": {
    "user_id": "uuid-5678",
    "email": "user@example.com",
    "reason": "too_many_failed_attempts"
  }
}
```

---

## 5. Event: Logout
### Name
`auth.logout`

### Description
Emitted when a refresh token is revoked (user logs out).  
Notification or analytics services may track this.

### Payload
```json
{
  "event": "auth.logout",
  "timestamp": "2025-08-17T12:15:00Z",
  "correlation_id": "uuid-5555",
  "producer": "auth-service",
  "data": {
    "user_id": "uuid-5678",
    "email": "user@example.com"
  }
}
```

---

## Notes
- All events include:
  - `event` → unique name of event
  - `timestamp` → UTC time of emission
  - `correlation_id` → trace ID across services
  - `producer` → always `auth-service`
  - `data` → event-specific payload
- Events are **fire-and-forget**: Auth service does not wait for subscriber response.
- Message broker: Kafka (preferred) or RabbitMQ (alternative).
