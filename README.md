# Strava Mileage Tracker

A web application for tracking running mileage and activities by integrating with the Strava API. Users can register, set mileage and long-run goals, connect their Strava account, and view their running activities in a personalized dashboard.

## Contributors
* Amanda McNesby
* Jeremiah Lezama
* William Kerr
* Tori Champagne

## Project Description

The Strava Mileage Tracker is a Flask-based web application that allows users to:
- Create user accounts with secure authentication
- Set personal mileage and long-run goals
- Connect their Strava account via OAuth 2.0
- Automatically sync running activities from Strava
- View their running activities and progress toward goals in a dashboard

The application uses SQLite for data storage, encrypts Strava tokens for security, and automatically refreshes access tokens when needed. Activities are synced from the last 30 days and displayed in a user-friendly interface.

## API Documentation

### Frontend Routes

#### `GET /`
- **Description:** Main dashboard page (requires authentication)
- **Method:** `GET`
- **Authentication:** Required (login_required)
- **Response:** Renders `index.html` template with user data
- **Behavior:** Automatically syncs Strava data if last sync was more than 15 minutes ago

#### `GET /login`
- **Description:** Login page
- **Method:** `GET`
- **Authentication:** Not required
- **Response:** Renders `login.html` template

#### `POST /login`
- **Description:** Authenticate user and create session
- **Method:** `POST`
- **Authentication:** Not required
- **Request Body (form data):**
  - `username` (string): User's username
  - `password` (string): User's password
- **Response:** 
  - Success: Redirects to dashboard (`/`)
  - Failure: Redirects to login page with error message

#### `GET /register`
- **Description:** Registration page
- **Method:** `GET`
- **Authentication:** Not required
- **Response:** Renders `register.html` template

#### `POST /register`
- **Description:** Create new user account
- **Method:** `POST`
- **Authentication:** Not required
- **Request Body (form data):**
  - `username` (string): Desired username (must be unique)
  - `password` (string): User's password (will be hashed)
  - `mileage` (float, optional): Weekly/monthly mileage goal
  - `long_run` (float, optional): Long run distance goal
- **Response:** 
  - Success: Creates user, logs them in, redirects to dashboard
  - Failure: Redirects to register page

#### `GET /logout`
- **Description:** Logout current user
- **Method:** `GET`
- **Authentication:** Required (login_required)
- **Response:** Logs out user and redirects to login page

### Strava Integration Routes

#### `GET /connect/strava`
- **Description:** Initiate Strava OAuth authorization flow
- **Method:** `GET`
- **Authentication:** Required (login_required)
- **Response:** Redirects to Strava authorization page
- **Note:** User will be redirected to Strava to authorize the application

#### `GET /strava/callback`
- **Description:** OAuth callback endpoint for Strava authorization
- **Method:** `GET`
- **Authentication:** Required (login_required)
- **Query Parameters:**
  - `code` (string): Authorization code from Strava (if successful)
  - `error` (string): Error code if authorization was denied
- **Response:** 
  - Success: Saves tokens, syncs activities, redirects to dashboard
  - Failure: Redirects to dashboard with error message

### API Endpoints

#### `GET /api/activities`
- **Description:** Get all activities, goals, and Strava connection status for the current user
- **Method:** `GET`
- **Authentication:** Required (login_required)
- **Response:** JSON object with the following structure:
  ```json
  {
    "activities": [
      {
        "activity_id": 123456789,
        "date": "2025-01-15",
        "distance": 5.2,
        "activity_title": "Morning Run"
      }
    ],
    "mileage_goal": 30.0,
    "long_run_goal": 8.0,
    "has_strava": true
  }
  ```
- **Response Fields:**
  - `activities` (array): List of activity objects, ordered by date (most recent first)
    - `activity_id` (integer): Strava activity ID
    - `date` (string): Activity date in YYYY-MM-DD format
    - `distance` (float): Distance in miles
    - `activity_title` (string): Title of the activity (may be "None")
  - `mileage_goal` (float): User's mileage goal
  - `long_run_goal` (float): User's long run goal
  - `has_strava` (boolean): Whether user has connected their Strava account

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- A Strava API application (for Strava integration)
  - Create at: https://www.strava.com/settings/api
  - You'll need: Client ID, Client Secret

### Environment Variables

Create a `.env` file in the project root directory with the following variables:

```env
FLASK_SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
STRAVA_CLIENT_ID=your-strava-client-id
STRAVA_CLIENT_SECRET=your-strava-client-secret
```

**Important:** 
- Never commit the `.env` file to version control
- Generate a secure `FLASK_SECRET_KEY` (e.g., using `python -c "import secrets; print(secrets.token_hex(32))"`)
- Generate a secure `ENCRYPTION_KEY` using Fernet (e.g., `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`)
- The `ENCRYPTION_KEY` must be a valid Fernet key (base64-encoded 32-byte key)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cs298f25/Amanda-Jeremaiah-William-Tori.git
   cd Amanda-Jeremaiah-William-Tori
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Create a `.env` file in the project root
   - Add all required environment variables (see above)

6. **Initialize the database:**
   ```bash
   python setup_db.py
   ```
   Or simply run the application (the database will be initialized automatically on first run via `database.init_db()` in `app.py`)

7. **Run the application:**
   ```bash
   python app.py
   ```
   
   The application will start on `http://0.0.0.0:8000` (accessible at `http://localhost:8000`)

8. **Access the application:**
   - Open your browser and navigate to: `http://localhost:8000`
   - Register a new account or log in with existing credentials

### Production Deployment

For production deployment on AWS EC2, see `deploy.md` for detailed instructions.

## Code Documentation

### Project Structure

```
Amanda-Jeremaiah-William-Tori/
├── app.py                 # Main Flask application and routes
├── database.py            # Database operations and SQLite management
├── collector.py           # Strava API integration and data collection
├── setup_db.py            # Database initialization script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── MileageTracker.db      # SQLite database (created at runtime)
├── static/                # Static files (CSS, JavaScript)
│   ├── style.css
│   ├── script.js
│   ├── login_script.js
│   └── register_script.js
├── templates/             # HTML templates
│   ├── index.html
│   ├── login.html
│   └── register.html
└── tests/                 # Unit tests
    ├── conftest.py
    ├── test_database.py
    └── test_collector.py
```

### Key Modules

#### `app.py`
Main Flask application file containing:
- Flask app initialization and configuration
- User authentication using Flask-Login
- Frontend route handlers (login, register, dashboard, logout)
- Strava OAuth integration routes
- API endpoint for activities data

**Key Classes:**
- `User`: UserMixin class for Flask-Login authentication

**Key Functions:**
- `load_user(user_id)`: Flask-Login user loader callback
- `dashboard()`: Main dashboard route with automatic sync logic
- `get_activities_data()`: API endpoint returning user activities and goals

#### `database.py`
Database operations module providing:
- SQLite database initialization and schema
- User management (create, authenticate, retrieve)
- Token encryption/decryption for Strava tokens
- Activity storage and retrieval
- Athlete goal management

**Key Functions:**
- `init_db()`: Creates database tables (Users, Athletes, DailyMileage)
- `encrypt_token(token)` / `decrypt_token(token)`: Secure token storage
- `create_user(username, password)`: Create new user with hashed password
- `validate_password(username, password)`: Verify user credentials
- `get_activities_for_user(user_id)`: Retrieve all activities for a user
- `save_user_tokens_and_info()`: Store encrypted Strava tokens

**Database Schema:**
- **Users**: id, username, password_hash, strava_athlete_id, strava_access_token, strava_refresh_token, token_expiration, last_sync_time
- **Athletes**: user_id (FK), mileage_goal, long_run_goal
- **DailyMileage**: user_id (FK), activity_id, date, distance, activity_title

#### `collector.py`
Strava API integration module handling:
- OAuth token exchange and refresh
- Activity fetching from Strava API
- Automatic token refresh when expired

**Key Functions:**
- `exchange_code_for_tokens(code)`: Exchange OAuth code for access/refresh tokens
- `authorize_and_save_user(code, user_id)`: Complete OAuth flow and save tokens
- `get_valid_access_token(user_id)`: Get valid access token, refreshing if needed
- `refresh_access_token(user_id, refresh_token)`: Refresh expired access token
- `fetch_and_save_user_data(user_id)`: Fetch last 30 days of activities from Strava and save to database

### Security Features

- **Password Hashing**: Uses Werkzeug's `pbkdf2:sha256` method for secure password storage
- **Token Encryption**: Strava tokens are encrypted using Fernet (symmetric encryption) before storage
- **Session Management**: Flask-Login handles secure session management
- **SQL Injection Prevention**: All database queries use parameterized statements

### Data Sync Behavior

- Activities are automatically synced when:
  - User connects their Strava account for the first time
  - User visits dashboard and last sync was more than 15 minutes ago
- Activities are fetched from the last 30 days
- Up to 50 activities per sync (Strava API limit)
- Distance is converted from meters to miles for display

## Testing

Run tests using pytest:

```bash
pytest tests/
```

Test files:
- `test_database.py`: Database operation tests
- `test_collector.py`: Strava integration tests

## Dependencies

See `requirements.txt` for complete list. Key dependencies:
- Flask 3.0.0 - Web framework
- Flask-Login 0.6.3 - User session management
- requests 2.31.0 - HTTP library for Strava API
- cryptography 42.0.5 - Token encryption
- python-dotenv 1.0.0 - Environment variable management
- gunicorn 23.0.0 - WSGI server for production

## License

This project is part of a web programming course assignment.
