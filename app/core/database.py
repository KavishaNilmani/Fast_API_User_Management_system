from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .config import DATABASE_URL, ADMIN_DATABASE_URL

try:
    print(f"Connecting to main database: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    # Test the main database connection
    with engine.connect() as connection:
        print("Main database connection successful!")
        
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Admin database connection
    print(f"Connecting to admin database: {ADMIN_DATABASE_URL}")
    admin_engine = create_engine(ADMIN_DATABASE_URL)
    
    # Test the admin database connection
    with admin_engine.connect() as connection:
        print("Admin database connection successful!")
        
    AdminSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=admin_engine)
    
    Base = declarative_base()
    
except SQLAlchemyError as e:
    print(f"Database connection failed: {e}")
    print("Please check your MySQL server and database configuration")
    raise
except Exception as e:
    print(f"Unexpected error: {e}")
    raise

# Dependency to get a main database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get an admin database session
def get_admin_db():
    db = AdminSessionLocal()
    try:
        yield db
    finally:
        db.close()
        