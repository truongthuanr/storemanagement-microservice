# Auth Service - Security

## 1. Password Security
- **Hashing Algorithm**: Use `bcrypt` or `argon2` for password hashing.  
- **Never store plain text passwords**.  
- **Salt**: Handled internally by `bcrypt`/`argon2`, no need to store separately unless required.  
- **Password Policy**:
  - Minimum length: 8 chars
  - At least 1 uppercase, 1 lowercase, 1 number
  - Disallow common/weak passwords

---

## 2. Token Strategy
### Access Token (JWT)
- Format: JWT (JSON Web Token)
- Signing Algorithm: **RS256** (preferred, public/private key)  
  - Private key in Auth service  
  - Public key shared to other services for verification  
- Payload (claims):
```json
{
  "sub": "uuid-of-user",
  "role": "user",
  "iat": 1692190329,
  "exp": 1692193929
}
```
- Expiry: **15 minutes** (short-lived)

### Refresh Token
- Random string (UUIDv4 / 256-bit secure random)
- Stored in DB with `expires_at`
- Expiry: **7 days**
- Stored hashed (optional, for security)

---

## 3. Token Lifecycle
- **Login**: Issue Access + Refresh token  
- **Refresh**: Rotate refresh token (old one revoked, new one issued)  
- **Logout**: Mark refresh token as revoked  
- **Compromised session**: Admin/user can revoke tokens via DB update  

---

## 4. Rate Limiting
- Apply per IP / per user on login endpoint:
  - e.g. **5 attempts / minute**
- Use Redis or in-memory limiter
- Return 429 Too Many Requests when exceeded

---

## 5. Account Locking
- If user fails login **5 times in a row** → lock account for 15 minutes  
- Emit event `auth.user_locked` for monitoring/notification
- Optional: allow manual unlock by admin

---

## 6. Transport Security
- All communication must be over **HTTPS/TLS**  
- No sensitive data in URL params (use body)  
- Secure cookies (if using cookies for refresh token storage)

---

## 7. Audit & Logging
- Log all authentication attempts:
  - user_id, IP, timestamp, success/fail
- Keep audit trail for compliance
- Ensure logs do not contain plain text passwords or secrets

---

## 8. Future Enhancements
- Multi-Factor Authentication (MFA / OTP)
- Social login via OAuth2 (Google, Facebook, Apple)
- Session management dashboard (admin can see active sessions)
