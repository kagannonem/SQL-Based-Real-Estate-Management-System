from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from pydantic import BaseModel
from auth import hash_password, verify_password, create_token, get_current_user, require_role
from dao.user_dao import UserDAO

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterInput(BaseModel):
    agent_id: int
    username: str
    password: str
    role: str  # 'admin' | 'manager' | 'agent'

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = UserDAO.get_by_username(form.username)
    if not user or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token({
        "sub": user["username"],
        "role": user["role"],
        "agent_id": user["AgentID"],
        "user_id": user["UserID"]
    })
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(data: RegisterInput, user=Depends(require_role("admin"))):
    hashed = hash_password(data.password)
    new_id = UserDAO.create_user(data.agent_id, data.username, hashed, data.role)
    return {"status": "success", "user_id": new_id}

@router.get("/me")
def me(user=Depends(get_current_user)):
    return user

@router.get("/users")
def list_users(user=Depends(require_role("admin"))):
    return {"status": "success", "data": UserDAO.get_all()}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, user=Depends(require_role("admin"))):
    success = UserDAO.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success"}