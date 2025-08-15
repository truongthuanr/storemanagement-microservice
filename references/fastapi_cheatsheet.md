
# Router
| Argument Type | Example                          | Source            |
| ------------- | -------------------------------- | ----------------- |
| Path param    | `user_id: int`                   | URL path          |
| Query param   | `page: int = 1`                  | URL `?page=1`     |
| Body param    | `payload: UserCreate`            | JSON body         |
| Dependency    | `db: Session = Depends(get_db)`  | Injected by DI    |
| Header        | `x_token: str = Header(...)`     | Request header    |
| Cookie        | `session_id: str = Cookie(None)` | Cookies           |
| Form          | `username: str = Form(...)`      | Form fields       |
| File upload   | `file: UploadFile = File(...)`   | Multipart/form    |
| Request       | `request: Request`               | Full request info |
| Response      | `response: Response`             | Mutate response   |


# Middleware 
| Middleware                | Mô tả                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------ |
| `CORSMiddleware`          | Xử lý CORS (Cross-Origin Resource Sharing).                                          |
| `GZipMiddleware`          | Tự động nén response bằng GZip để giảm dung lượng truyền tải.                        |
| `TrustedHostMiddleware`   | Chỉ cho phép truy cập từ các `Host` cụ thể (phòng chống HTTP Host header attacks).   |
| `HTTPSRedirectMiddleware` | Tự động redirect HTTP → HTTPS (chỉ dùng nếu bạn không dùng reverse proxy như nginx). |
| `SessionMiddleware`       | Hỗ trợ session cookie (dùng cho các app stateful).                                   |
| `BaseHTTPMiddleware`      | Base class để bạn tạo custom middleware của riêng mình.                              |



# Example
# Router
```
from fastapi import (
    APIRouter, Depends, Query, Path, Header, Cookie, Form, File, UploadFile,
    Request, Response, HTTPException, status
)
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

@router.post(
    "/demo/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Demo all FastAPI parameter types"
)
async def demo_all_params(
    # Path parameter
    user_id: int = Path(..., ge=1, description="ID of the user"),

    # Query parameter
    q: Optional[str] = Query(None, max_length=50, description="Search keyword"),
    lang: str = Query("en", description="Language"),

    # Header
    user_agent: Optional[str] = Header(None),
    x_token: Optional[str] = Header(None, alias="X-Token"),

    # Cookie
    session_id: Optional[str] = Cookie(None),

    # Form
    username: str = Form(...),
    password: str = Form(...),

    # File Upload
    profile_pic: UploadFile = File(...),

    # Request body
    payload: UserCreate = Depends(),  # Dùng Depends để ép tách payload khỏi multipart/form

    # Request and response objects
    request: Request,
    response: Response,

    # Dependency (DB)
    db: Session = Depends(get_db)
):
    # Log a few details
    client_ip = request.client.host
    response.headers["X-Debug"] = "true"

    # Validate token
    if x_token != "secrettoken":
        raise HTTPException(status_code=401, detail="Invalid X-Token")

    # Save file (mock logic)
    file_content = await profile_pic.read()
    if len(file_content) > 1_000_000:
        raise HTTPException(status_code=413, detail="File too large")

    # Simulate saving user to DB
    fake_user = {
        "id": user_id,
        "name": payload.name,
        "email": payload.email
    }

    return fake_user
```