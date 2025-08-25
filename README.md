# FastAPI User Management System

A modern, secure user management system built with FastAPI, featuring user authentication, admin panel, and a Streamlit frontend interface.

## 🚀 Features

- **User Management**: Create, read, update, and delete user accounts
- **Admin Panel**: Secure admin interface with user management capabilities
- **Authentication**: JWT-based authentication system
- **Database**: MySQL database with separate admin and user databases
- **Frontend**: Streamlit-based web interface
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Security**: Password hashing, input validation, and role-based access control

## 🏗️ Architecture

```
Fast_API_App/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── crud/
│       ├── __init__.py
│       └── crud.py
├── run_app.py
├── requirements.txt
└── frontend.py
```

## 📋 Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Fast_API_App
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL databases**
   - Create a database named `fastapi_db` for users
   - Create a database named `admin_db` for admin accounts
   - Ensure MySQL server is running on localhost:3306

4. **Configure environment variables**
   - Update database credentials in `app/core/config.py` if needed
   - Default configuration:
     - Main DB: `mysql+mysqlconnector://root:root@localhost:3306/fastapi_db`
     - Admin DB: `mysql+mysqlconnector://root:root@localhost:3306/admin_db`

## 🚀 Running the Application

### Option 1: Use the Launcher Script (Recommended)
```bash
python run_app.py
```

Choose from the menu:
- **Option 1**: Start Backend (FastAPI) only
- **Option 2**: Start Frontend (Streamlit) only  
- **Option 3**: Start Both (Backend + Frontend)
- **Option 4**: Exit

### Option 2: Manual Start

**Start Backend:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Start Frontend:**
```bash
streamlit run frontend.py --server.port 8501
```

## 🌐 Access Points

- **Backend API**: http://localhost:8001
- **Frontend Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8001/docs
- **Admin Dashboard**: http://localhost:8001/admin

## 📚 API Endpoints

### Public Endpoints
- `POST /users` - Create new user account
- `POST /login` - User login
- `GET /docs` - API documentation

### Protected Endpoints (Require Authentication)
- `GET /me` - Get current user profile
- `PUT /users/{user_id}` - Update user profile
- `DELETE /users/{user_id}` - Delete user account

### Admin Endpoints (Require Admin Authentication)
- `POST /admin/login` - Admin login
- `GET /admin` - Admin dashboard
- `GET /admin/me` - Admin profile
- `POST /admin/users` - Create user (admin only)
- `GET /admin/users` - Get all users
- `GET /admin/users/{user_id}` - Get specific user
- `PUT /admin/users/{user_id}` - Update user (admin only)
- `DELETE /admin/users/{user_id}` - Delete user (admin only)

## 🔐 Authentication

The system uses JWT (JSON Web Tokens) for authentication:

1. **User Login**: Send credentials to `/login` endpoint
2. **Admin Login**: Send credentials to `/admin/login` endpoint
3. **Use Token**: Include `Authorization: Bearer <token>` header in subsequent requests

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email (must end with .com)
- `hashed_password`: Encrypted password
- `is_admin`: Admin status flag

### Admins Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `hashed_password`: Encrypted password
- `is_super_admin`: Super admin flag

## 🔧 Configuration

Key configuration options in `app/core/config.py`:

- `DATABASE_URL`: Main database connection string
- `ADMIN_DATABASE_URL`: Admin database connection string
- `SECRET_KEY`: JWT signing secret
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## 🧪 Testing

Test the API endpoints using:

1. **Swagger UI**: http://localhost:8001/docs
2. **Frontend Interface**: http://localhost:8501
3. **cURL commands**:
   ```bash
   # Create user
   curl -X POST "http://localhost:8001/users" \
        -H "Content-Type: application/json" \
        -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
   
   # Login
   curl -X POST "http://localhost:8001/login" \
        -H "Content-Type: application/json" \
        -d '{"username":"testuser","password":"password123"}'
   ```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL server is running
   - Check database credentials in config.py
   - Verify databases exist

2. **Import Errors**
   - Ensure all `__init__.py` files are present
   - Check Python path and working directory

3. **Port Already in Use**
   - Change ports in run_app.py or use different ports
   - Kill existing processes using the ports

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export PYTHONPATH=.
python -c "from app.main import app; print('Debug mode enabled')"
```

## 📝 Development

### Adding New Endpoints

1. Create new route in `app/main.py`
2. Add corresponding schema in `app/schemas/schemas.py`
3. Implement CRUD operations in `app/crud/crud.py`
4. Update models if needed in `app/models/models.py`

### Database Migrations

For schema changes:
1. Update models in `app/models/models.py`
2. Restart the application (tables are auto-created)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the code structure in the `app/` directory
- Ensure all dependencies are properly installed

---

