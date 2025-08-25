from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .core.database import Base, engine, get_db, get_admin_db
from .models.models import User, Admin
from .schemas.schemas import UserCreate, UserUpdate, UserResponse, Token, AdminCreate, AdminLogin, AdminResponse
from .crud.crud import create_user, update_user, delete_user, authenticate_user, get_user_by_username, create_admin, authenticate_admin, get_all_users, get_user_by_id
from .api.auth import create_access_token, get_current_user, get_current_admin, require_admin_access
from datetime import timedelta
from .core.config import ACCESS_TOKEN_EXPIRE_MINUTES

# Create tables in both databases
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API with Admin Panel")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        if error["type"] == "value_error":
            errors.append(f"{error['loc'][-1]}: {error['msg']}")
        else:
            errors.append(f"{error['loc'][-1]}: {error['msg']}")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": errors,
            "message": "Please check your input data. Email must contain '@' and end with '.com'"
        }
    )

# ==================== ADMIN ENDPOINTS ====================

# Admin Dashboard (Simple info page)
@app.get("/admin")
def admin_dashboard():
    return {
        "message": "Admin Dashboard",
        "available_endpoints": {
            "admin_login": "POST /admin/login",
            "admin_create_user": "POST /admin/users",
            "admin_get_all_users": "GET /admin/users",
            "admin_get_user": "GET /admin/users/{user_id}",
            "admin_update_user": "PUT /admin/users/{user_id}",
            "admin_delete_user": "DELETE /admin/users/{user_id}",
            "admin_profile": "GET /admin/me"
        },
        "note": "Use POST /admin/login to authenticate and get access token"
    }

# Admin Login
@app.post("/admin/login", response_model=Token)
def admin_login_for_access_token(form_data: AdminLogin, db: Session = Depends(get_admin_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid Admin Username or Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": admin.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Admin Create User (Admin only)
@app.post("/admin/users", response_model=UserResponse)
def admin_create_user(user: UserCreate, db: Session = Depends(get_db), current_admin = Depends(require_admin_access)):
    print(f"=== ADMIN CREATE USER REQUEST RECEIVED ===")
    print(f"Admin: {current_admin.username}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Password length: {len(user.password) if user.password else 0}")
    
    try:
        # Validate email format
        if user.email:
            if not user.email.endswith('.com') or '@' not in user.email:
                raise HTTPException(
                    status_code=400, 
                    detail="Email must contain '@' and end with '.com'"
                )
        
        print("Checking if username already exists...")
        db_user = get_user_by_username(db, user.username)
        if db_user:
            print(f"Username {user.username} already exists")
            raise HTTPException(status_code=400, detail="Username already exists")
        
        print(f"Username is available, creating new user: {user.username}")
        result = create_user(db, user.username, user.email, user.password, user.is_admin)
        print(f"User created successfully: {result.username}")
        print(f"User ID: {result.id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR creating user: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin Update User (Admin only)
@app.put("/admin/users/{user_id}", response_model=UserResponse)
def admin_update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_admin = Depends(require_admin_access)):
    try:
        # Validate email format if email is being updated
        if user.email:
            if not user.email.endswith('.com') or '@' not in user.email:
                raise HTTPException(
                    status_code=400, 
                    detail="Email must contain '@' and end with '.com'"
                )
        
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return update_user(db, db_user, user.username, user.email, user.password, user.is_admin)
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR updating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin Delete User (Admin only)
@app.delete("/admin/users/{user_id}")
def admin_delete_user(user_id: int, db: Session = Depends(get_db), current_admin = Depends(require_admin_access)):
    try:
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        delete_user(db, db_user)
        return {"detail": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin Get All Users (Admin only)
@app.get("/admin/users", response_model=list[UserResponse])
def admin_get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin = Depends(require_admin_access)):
    users = get_all_users(db, skip=skip, limit=limit)
    return users

# Admin Get User by ID (Admin only)
@app.get("/admin/users/{user_id}", response_model=UserResponse)
def admin_get_user_by_id(user_id: int, db: Session = Depends(get_db), current_admin = Depends(require_admin_access)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Admin Get Current Admin Info
@app.get("/admin/me", response_model=AdminResponse)
def read_current_admin(current_admin = Depends(get_current_admin)):
    return current_admin

# ==================== USER ENDPOINTS ====================

# Create User (Regular user registration)
@app.post("/users", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    print(f"=== CREATE USER REQUEST RECEIVED ===")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Password length: {len(user.password) if user.password else 0}")
    
    try:
        # Validate email format
        if user.email:
            if not user.email.endswith('.com') or '@' not in user.email:
                raise HTTPException(
                    status_code=400, 
                    detail="Email must contain '@' and end with '.com'"
                )
        
        print("Checking if username already exists...")
        db_user = get_user_by_username(db, user.username)
        if db_user:
            print(f"Username {user.username} already exists")
            raise HTTPException(status_code=400, detail="Username already exists")
        
        print(f"Username is available, creating new user: {user.username}")
        # Regular users cannot create admin accounts
        result = create_user(db, user.username, user.email, user.password, is_admin=False)
        print(f"User created successfully: {result.username}")
        print(f"User ID: {result.id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR creating user: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

# Update User (User can update their own profile)
@app.put("/users/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        # Users can only update their own profile
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="You can only update your own profile")
        
        # Validate email format if email is being updated
        if user.email:
            if not user.email.endswith('.com') or '@' not in user.email:
                raise HTTPException(
                    status_code=400, 
                    detail="Email must contain '@' and end with '.com'"
                )
        
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Regular users cannot change their admin status
        if user.is_admin is not None:
            user.is_admin = current_user.is_admin
        
        return update_user(db, db_user, user.username, user.email, user.password, user.is_admin)
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR updating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Delete User (User can delete their own account)
@app.delete("/users/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        # Users can only delete their own account
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="You can only delete your own account")
        
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        delete_user(db, db_user)
        return {"detail": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Login 
@app.post("/login", response_model=Token)
def login_for_access_token(form_data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Username or Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Route Example
@app.get("/me", response_model=UserResponse)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user
