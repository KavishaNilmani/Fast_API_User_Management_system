import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="FastAPI User Management",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def make_api_request(endpoint, method="GET", data=None, headers=None):
    """Make API request to FastAPI backend"""
    url = f"{API_BASE_URL}{endpoint}"
    
    if headers is None:
        headers = {}
    
    if st.session_state.access_token:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
    
    try:
        # Add timeout to prevent hanging requests
        timeout = 10  # 10 seconds timeout
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=timeout)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=timeout)
        
        return response
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the FastAPI backend. Please make sure it's running on http://localhost:8000")
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. The API is taking too long to respond.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def test_backend_connection():
    """Test if the backend is reachable"""
    st.info("Testing backend connection...")
    response = make_api_request("/health")
    
    if response and response.status_code == 200:
        st.success("✅ Backend connection successful!")
        st.json(response.json())
        return True
    else:
        st.error("❌ Backend connection failed!")
        return False

def login_user(username, password):
    """Login user and get access token"""
    data = {"username": username, "password": password}
    response = make_api_request("/login", method="POST", data=data)
    
    if response and response.status_code == 200:
        token_data = response.json()
        st.session_state.access_token = token_data["access_token"]
        st.session_state.current_user = username
        st.success("Login successful!")
        st.rerun()
    elif response:
        st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")

def logout_user():
    """Logout user"""
    st.session_state.access_token = None
    st.session_state.current_user = None
    st.success("Logout successful!")
    st.rerun()

def create_user(username, email, password):
    """Create a new user"""
    data = {"username": username, "email": email, "password": password}
    
    # Debug information
    st.info(f"Attempting to create user: {username} with email: {email}")
    st.info(f"API URL: {API_BASE_URL}/users")
    st.info(f"Request data: {data}")
    
    response = make_api_request("/users", method="POST", data=data)
    
    if response and response.status_code == 200:
        user_data = response.json()
        st.success(f"User '{username}' created successfully!")
        return user_data
    elif response:
        error_detail = response.json().get('detail', 'Unknown error')
        st.error(f"Failed to create user: {error_detail}")
        st.error(f"Status code: {response.status_code}")
        st.error(f"Response: {response.text}")
    else:
        st.error("No response received from the API")
        st.error("This usually means:")
        st.error("1. The backend is not running")
        st.error("2. There's a network connectivity issue")
        st.error("3. The request timed out")
        st.error("4. There's a firewall blocking the connection")
    return None

def update_user(user_id, username, email, password):
    """Update an existing user"""
    data = {}
    if username:
        data["username"] = username
    if email:
        data["email"] = email
    if password:
        data["password"] = password
    
    if not data:
        st.warning("Please provide at least one field to update")
        return None
    
    response = make_api_request(f"/users/{user_id}", method="PUT", data=data)
    
    if response and response.status_code == 200:
        user_data = response.json()
        st.success(f"User updated successfully!")
        return user_data
    elif response:
        st.error(f"Failed to update user: {response.json().get('detail', 'Unknown error')}")
    return None

def delete_user(user_id):
    """Delete a user"""
    response = make_api_request(f"/users/{user_id}", method="DELETE")
    
    if response and response.status_code == 200:
        st.success("User deleted successfully!")
        return True
    elif response:
        st.error(f"Failed to delete user: {response.json().get('detail', 'Unknown error')}")
    return False

def get_current_user_info():
    """Get current user information"""
    response = make_api_request("/me")
    
    if response and response.status_code == 200:
        return response.json()
    return None

# Main application
def main():
    st.markdown('<h1 class="main-header">👥 FastAPI User Management System</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("🔧 Navigation")
    
    if st.session_state.access_token:
        st.sidebar.success(f"Logged in as: {st.session_state.current_user}")
        if st.sidebar.button("Logout"):
            logout_user()
        
        # Navigation options for logged-in users
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["Dashboard", "User Management", "Create User", "Update User", "Delete User", "My Profile"]
        )
    else:
        st.sidebar.info("Please login to access the system")
        page = "Login"
    
    # Page routing
    if st.session_state.get('page') == "Create User":
        show_create_user()
    elif st.session_state.get('page') == "Update User":
        show_update_user()
    elif st.session_state.get('page') == "Delete User":
        show_delete_user()
    elif page == "Login":
        show_login_page()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "User Management":
        show_user_management()
    elif page == "My Profile":
        show_my_profile()

def show_login_page():
    """Display login page"""
    st.markdown("## User Authentication")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Instructions:</h4>
            <ul>
                <li>Make sure your FastAPI backend is running on http://localhost:8000</li>
                <li>Use existing credentials or create a new user first</li>
                <li>After login, you can access all CRUD operations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Test backend connection button
        if st.button("🔍 Test Backend Connection", use_container_width=True):
            test_backend_connection()
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button and username and password:
                login_user(username, password)
        
        # Create Account button (outside the form)
        if st.button("Create New Account", use_container_width=True):
            st.session_state.show_create_account = True
        
        # Show create account form if requested
        if st.session_state.get('show_create_account', False):
            st.markdown("---")
            st.markdown("### Create New Account")
            
            with st.form("create_account_form"):
                new_username = st.text_input("New Username", placeholder="Enter new username")
                new_email = st.text_input("New Email", placeholder="Enter email address")
                new_password = st.text_input("New Password", type="password", placeholder="Enter new password")
                
                col1, col2 = st.columns(2)
                with col1:
                    create_button = st.form_submit_button("Create Account", use_container_width=True)
                with col2:
                    cancel_button = st.form_submit_button("Cancel", use_container_width=True)
                
                if create_button:
                    if new_username and new_email and new_password:
                        user_data = create_user(new_username, new_email, new_password)
                        if user_data:
                            st.session_state.show_create_account = False
                            st.success("Account created! You can now login.")
                            st.rerun()
                    else:
                        st.warning("Please fill all fields")
                
                if cancel_button:
                    st.session_state.show_create_account = False
                    st.rerun()

def show_dashboard():
    """Display dashboard with system overview"""
    st.markdown("## Dashboard")
    
    # Get current user info
    current_user_info = get_current_user_info()
    
    if current_user_info:
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Current User</h3>
                <h2>{}</h2>
            </div>
            """.format(current_user_info["username"]), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>Email</h3>
                <h4>{}</h4>
            </div>
            """.format(current_user_info["email"]), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>User ID</h3>
                <h2>{}</h2>
            </div>
            """.format(current_user_info["id"]), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Create New User", use_container_width=True):
                st.session_state.page = "Create User"
                st.rerun()
        
        with col2:
            if st.button("Update User", use_container_width=True):
                st.session_state.page = "Update User"
                st.rerun()
        
        with col3:
            if st.button("Delete User", use_container_width=True):
                st.session_state.page = "Delete User"
                st.rerun()
        
        # System status
        st.markdown("---")
        st.markdown("### System Status")
        
        # Test API connection
        response = make_api_request("/me")
        if response and response.status_code == 200:
            st.success("Backend API is running and accessible")
        else:
            st.error("Backend API is not accessible")
        
        # Current session info
        st.info(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.info(f"Token type: Bearer")

def show_user_management():
    """Display user management overview"""
    st.markdown("## User Management")
    
    st.markdown("""
    <div class="info-box">
        <h4>📋 Available Operations:</h4>
        <ul>
            <li><strong>Create User:</strong> Add new users to the system</li>
            <li><strong>Update User:</strong> Modify existing user information</li>
            <li><strong>Delete User:</strong> Remove users from the system</li>
            <li><strong>View Profile:</strong> Check your current user information</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current user info
    current_user_info = get_current_user_info()
    if current_user_info:
        st.markdown("### Current User Information")
        user_df = pd.DataFrame([current_user_info])
        st.dataframe(user_df, use_container_width=True)
    
    # API endpoints information
    st.markdown("---")
    st.markdown("### Available API Endpoints")
    
    endpoints_info = {
        "POST /users": "Create a new user",
        "PUT /users/{user_id}": "Update an existing user",
        "DELETE /users/{user_id}": "Delete a user",
        "POST /login": "User authentication",
        "GET /me": "Get current user information"
    }
    
    for endpoint, description in endpoints_info.items():
        st.markdown(f"**`{endpoint}`** - {description}")

def show_create_user():
    """Display create user form"""
    st.markdown("## Create New User")
    
    # Back to dashboard button
    if st.button("← Back to Dashboard"):
        st.session_state.page = None
        st.rerun()
    
    st.markdown("""
    <div class="info-box">
        <h4>Instructions:</h4>
        <ul>
            <li>Fill in all required fields</li>
            <li>Username and email must be unique</li>
            <li>Password will be securely hashed</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("create_user_form"):
        username = st.text_input("Username *", placeholder="Enter username")
        email = st.text_input("Email *", placeholder="Enter email address")
        password = st.text_input("Password *", type="password", placeholder="Enter password")
        confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Create User", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("Clear Form", use_container_width=True)
        
        if submit_button:
            if not all([username, email, password, confirm_password]):
                st.error("Please fill all required fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                user_data = create_user(username, email, password)
                if user_data:
                    st.markdown("---")
                    st.markdown("### User Created Successfully")
                    user_df = pd.DataFrame([user_data])
                    st.dataframe(user_df, use_container_width=True)

def show_update_user():
    """Display update user form"""
    st.markdown("## Update User")
    
    # Back to dashboard button
    if st.button("← Back to Dashboard"):
        st.session_state.page = None
        st.rerun()
    
    st.markdown("""
    <div class="info-box">
        <h4>Instructions:</h4>
        <ul>
            <li>Enter the User ID you want to update</li>
            <li>Only fill the fields you want to change</li>
            <li>Leave fields empty to keep current values</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("update_user_form"):
        user_id = st.number_input("User ID *", min_value=1, placeholder="Enter user ID to update")
        
        st.markdown("### Update Fields (leave empty to keep current values)")
        username = st.text_input("New Username", placeholder="Enter new username (optional)")
        email = st.text_input("New Email", placeholder="Enter new email (optional)")
        password = st.text_input("New Password", type="password", placeholder="Enter new password (optional)")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Update User", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("Clear Form", use_container_width=True)
        
        if submit_button:
            if not user_id:
                st.error("Please enter a User ID")
            elif not any([username, email, password]):
                st.error("Please provide at least one field to update")
            else:
                user_data = update_user(user_id, username, email, password)
                if user_data:
                    st.markdown("---")
                    st.markdown("### User Updated Successfully")
                    user_df = pd.DataFrame([user_data])
                    st.dataframe(user_df, use_container_width=True)

def show_delete_user():
    """Display delete user form"""
    st.markdown("## Delete User")
    
    # Back to dashboard button
    if st.button("← Back to Dashboard"):
        st.session_state.page = None
        st.rerun()
    
    st.markdown("""
    <div class="warning-box">
        <h4>Warning:</h4>
        <ul>
            <li>This action cannot be undone</li>
            <li>All user data will be permanently deleted</li>
            <li>Make sure you have the correct User ID</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("delete_user_form"):
        user_id = st.number_input("User ID *", min_value=1, placeholder="Enter user ID to delete")
        
        # Confirmation checkbox
        confirm_delete = st.checkbox("I understand this action cannot be undone")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Delete User", use_container_width=True, disabled=not confirm_delete)
        with col2:
            clear_button = st.form_submit_button("Clear Form", use_container_width=True)
        
        if submit_button:
            if not user_id:
                st.error("Please enter a User ID")
            elif not confirm_delete:
                st.error("Please confirm the deletion")
            else:
                # Double confirmation
                if st.button("Confirm Deletion (Click Again)"):
                    success = delete_user(user_id)
                    if success:
                        st.success("User deleted successfully!")

def show_my_profile():
    """Display current user profile"""
    st.markdown("## My Profile")
    
    current_user_info = get_current_user_info()
    
    if current_user_info:
        st.markdown("### User Information")
        
        # Display user info in a nice format
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Profile</h3>
                <h2>{}</h2>
                <p>User ID: {}</p>
            </div>
            """.format(current_user_info["username"], current_user_info["id"]), unsafe_allow_html=True)
        
        with col2:
            user_df = pd.DataFrame([current_user_info])
            st.dataframe(user_df, use_container_width=True)
        
        # Session information
        st.markdown("---")
        st.markdown("### Session Information")
        
        session_info = {
            "Username": current_user_info["username"],
            "User ID": current_user_info["id"],
            "Email": current_user_info["email"],
            "Login Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Token Type": "Bearer",
            "Token Status": "Valid" if st.session_state.access_token else "Invalid"
        }
        
        session_df = pd.DataFrame(list(session_info.items()), columns=["Property", "Value"])
        st.dataframe(session_df, use_container_width=True)
        
        # Actions
        st.markdown("---")
        st.markdown("### Profile Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Refresh Profile", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("Logout", use_container_width=True):
                logout_user()
    else:
        st.error("Unable to fetch user profile information")

if __name__ == "__main__":
    main()
