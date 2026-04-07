# 🗳️ Online Voting System

[![CI/CD Pipeline](https://github.com/Jokimpr/online-voting-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Jokimpr/online-voting-api/actions/workflows/ci-cd.yml)

A clean, production-ready online voting application built with Flask, featuring separate admin and student roles, secure authentication, and SQLite database.

## Features ✨

- **Dual Role System**: Separate admin and student interfaces
- **Secure Authentication**: Password hashing with werkzeug.security
- **Voter ID System**: Automatic extraction from college email addresses
- **Email Validation**: Only @kristujayanti.com emails allowed
- **Vote Prevention**: One vote per user with has_voted flag
- **Admin Dashboard**: Add/delete candidates, view statistics
- **Real-time Results**: Live vote counting and winner display
- **Responsive UI**: Clean, modern interface
- **SQLite Database**: Simple, file-based database

## Project Structure

```
online-voting-api/
├── run.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── voting_system.db       # SQLite database (auto-created)
├── README.md             # This file
├── static/               # Static files (CSS, JS, images)
└── templates/
    ├── login.html        # Student login page
    ├── register.html     # Student registration page
    ├── admin_login.html  # Admin login page
    ├── admin_dashboard.html # Admin management page
    ├── vote.html         # Voting page
    └── results.html      # Results display page
```

## Installation

### Prerequisites

- Python 3.9 or higher

### Setup

1. **Navigate to project directory**
   ```bash
   cd online-voting-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   - Student Portal: http://localhost:5000/
   - Admin Portal: http://localhost:5000/admin/login

## Usage

### Admin Setup
- Default admin credentials: `admin` / `admin123`
- **Important**: Change the default password in production!

### Student Registration
- Students must register with college email (@kristujayanti.com)
- Voter ID is automatically extracted from email prefix
- Example: `23bcnb31@kristujayanti.com` → Voter ID: `23bcnb31`

### Voting Process
1. Student registers/logs in with voter ID
2. Selects a candidate from the list
3. Votes once (prevented from voting again)
4. Views results after voting

### Admin Functions
- Login to admin dashboard
- Add new candidates with name, department, position
- Delete candidates
- View voting statistics
- Access detailed results

## Database Schema

### Users Table
- id (Primary Key)
- voter_id (Unique, from email)
- email (College domain only)
- password_hash (Hashed)
- has_voted (Boolean)

### Admin Table
- id (Primary Key)
- username (Unique)
- password_hash (Hashed)

### Candidates Table
- id (Primary Key)
- name
- department
- position
- vote_count (Default 0)

## Security Features

- Password hashing using werkzeug.security
- Parameterized SQL queries to prevent injection
- Session-based authentication
- Email domain validation
- Vote prevention mechanism

## API Endpoints

### Student Routes
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET/POST /vote` - Cast vote
- `GET /results` - View results
- `GET /logout` - Logout

### Admin Routes
- `GET/POST /admin/login` - Admin login
- `GET /admin/dashboard` - Admin dashboard
- `POST /admin/add_candidate` - Add candidate
- `POST /admin/delete_candidate/<id>` - Delete candidate
- `GET /admin/results` - Admin results view
- `GET /admin/logout` - Admin logout

## Development

### Running Tests
```bash
# No tests included in minimal version
```

### Database Reset
Delete `voting_system.db` file to reset all data.

## Production Deployment

1. Change default admin password in `run.py`
2. Set `app.config['SECRET_KEY']` to a secure random string
3. Consider using a production WSGI server (gunicorn)
4. Use environment variables for sensitive data
5. Enable HTTPS in production

## DevOps Pipeline

### 🐳 Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up --build
```

**Services:**
- **Flask App**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### 📊 Monitoring & Metrics
- Prometheus scrapes metrics from `/metrics` endpoint
- Grafana dashboards show voting statistics and system metrics

### 🧪 Testing
```bash
# Run Selenium tests
pytest tests/test_selenium.py

# Run API tests in Jupyter
jupyter notebook voting_system_tests.ipynb
```

### 📈 Metrics Tracked
- Total votes cast
- User registrations
- Admin logins
- User logins
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set a strong `SECRET_KEY`:
   ```
   SECRET_KEY=your-strong-secret-key-here
   ```

5. **Run the application**
   ```bash
   flask run
   ```
   
   The app will be available at `http://localhost:5000`

### Docker Setup

1. **Create .env file**
   ```bash
   cp .env.example .env
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```
   
   The app will be available at `http://localhost:5000`

3. **To stop the containers**
   ```bash
   docker-compose down
   ```

## Usage 🎯

### 1. **Register an Account**
   - Go to the registration page
   - Create a new account with username, email, and password
   - Passwords must be at least 6 characters

### 2. **Add Voters**
   - After logging in, add voters using their voter IDs
   - Each voter ID must be unique

### 3. **Add Candidates**
   - Add candidates who will appear on the ballot
   - Candidates are stored per user

### 4. **Cast Votes**
   - Voters can select a candidate and cast their vote
   - Each voter can only vote once
   - Vote is immediately recorded

### 5. **View Results**
   - Results are displayed in real-time
   - Vote counts are updated after each vote

### 6. **Export Results**
   - Download voting results as an Excel file
   - Includes candidate names and vote counts

### 7. **Reset Data**
   - Clear all voters, candidates, and votes
   - This action cannot be undone

## Technology Stack 🛠️

- **Backend**: Flask 2.3.3
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login with Werkzeug
- **Frontend**: HTML5, CSS3
- **Export**: Pandas & OpenPyXL
- **Containerization**: Docker & Docker Compose

## Key Improvements 🚀

Compared to the original version, this update includes:

1. **Persistent Storage**: Data survives application restarts
2. **User Authentication**: Login/registration system
3. **Security**: Password hashing and user isolation
4. **Database Models**: Proper ORM structure with relationships
5. **Docker Support**: Easy deployment and scaling
6. **Enhanced UI**: Modern, responsive interface
7. **Error Handling**: Proper error pages and flash messages
8. **Session Management**: User sessions with Flask-Login

## Environment Variables 🔐

- `FLASK_APP`: Application entry point (default: run.py)
- `FLASK_ENV`: Environment mode (development/production)
- `SECRET_KEY`: Secret key for session management (MUST BE CHANGED IN PRODUCTION)
- `DATABASE_URL`: Database connection string (default: SQLite)

## Database Schema 📊

### Users Table
- id, username, email, password_hash, is_admin, created_at

### Voters Table
- id, user_id, voter_id, created_at

### Candidates Table
- id, name, created_by, created_at

### Votes Table
- id, voter_id, candidate_id, created_at

## API-like Routes

- `POST /register` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout
- `GET / (POST /)` - Main voting page
- `GET /export` - Export results as Excel
- `POST /reset` - Reset all user data

## Troubleshooting 🔧

### Database Issues
- Delete `voting_system.db` to reset the database
- Tables will be recreated automatically on app startup

### Login Issues
- Ensure `.env` file has `SECRET_KEY` set
- Check database is in correct location

### Docker Issues
```bash
# View logs
docker-compose logs web

# Rebuild containers
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v
```

## Security Recommendations ⚠️

1. Change `SECRET_KEY` in production
2. Use HTTPS in production
3. Set `FLASK_ENV=production` in production
4. Use PostgreSQL instead of SQLite for production
5. Implement rate limiting
6. Add CSRF protection for forms

## Future Enhancements 🔮

- Email verification for registration
- Two-factor authentication
- Voting polls/campaigns management
- Admin dashboard
- Real-time voting updates with WebSockets
- Voting analytics and charts
- Multi-language support

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues or questions, feel free to reach out!

---

**Built with ❤️ for secure voting systems**
