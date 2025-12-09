# Hospital Insight Hub

Hospital Insight Hub is a small, full-stack Flask application that sits between a hospital’s admissions desk and its analytics team. It lets staff:

- Sign in securely
- Manage stroke-related patient records
- Explore the Kaggle stroke dataset through summaries and charts
- Keep a basic audit trail of activity

The project is designed as a teaching and portfolio piece for **secure web development with data handling** rather than a clinical decision tool.

---

## 1. Quick project snapshot

| Item                  | Detail                                                |
|-----------------------|-------------------------------------------------------|
| Framework             | Flask (application factory pattern)                   |
| Frontend              | Jinja2 templates + Bootstrap + custom CSS            |
| Auth store            | SQLite (Flask-SQLAlchemy)                             |
| Clinical data store   | MongoDB Atlas (`patients`, `activity_log` collections)|
| Analytics             | Pandas, Matplotlib, Seaborn                           |
| Dataset               | Kaggle “Healthcare Dataset Stroke Data”              |
| Tests                 | Pytest (6 tests across auth and protected routes)     |

---

## 2. What this application demonstrates

The app is intentionally small but touches several “real world” concerns:

- **Separation of concerns**
  - Users and logins live in SQLite.
  - Clinical data lives in MongoDB Atlas.
- **Secure programming habits**
  - Password hashing, CSRF protection, login-required routes.
  - Configuration and secrets in `.env`, not hard-coded.
- **Data literacy**
  - Data overview page with preview, missing values, summary statistics and outlier counts.
  - Visual summaries (gender distribution, stroke outcome split, age/BMI distributions, correlation heatmap).
- **Operational transparency**
  - Activity log that records key actions such as patient creates/updates/deletes and dataset uploads.
- **Basic test suite**
  - Pytest used to confirm authentication pages load and that key routes are protected.

---

## 3. Core features in a bit more detail

### 3.1 User accounts and sessions

- Users register via a simple registration form.
- Credentials are hashed before being stored in SQLite.
- Login and logout are handled with `Flask-Login`.
- Only authenticated and active users can:
  - View or edit patient records
  - See data overview and visualisations
  - Upload a new dataset

A small profile page allows a logged-in user to adjust basic details like display name and email.

---

### 3.2 Patient record management (MongoDB)

Stroke-related patient records are stored in MongoDB Atlas. Through the UI, a logged-in user can:

- View a **patient list** with:
  - ID, gender, age, hypertension, heart disease, stroke status
  - Search by patient ID
- Create a new patient record via a structured form
- Edit an existing record
- Delete a record (with confirmation)

The design keeps the layout clean and table-driven while still showing enough clinical attributes for simple data exploration.

---

### 3.3 Data overview for the stroke dataset

A dedicated **Data Overview** section provides:

- Preview of the first rows of the dataset
- Table of missing values per column
- Descriptive statistics for numeric columns (mean, min, max, quartiles)
- Outlier counts per column using the IQR method
- Textual notes about why data quality, missing values and outliers matter in a healthcare context

All of this is driven from a CSV located at:

dataset/healthcare-dataset-stroke-data.csv
The path is configurable via an environment variable if needed.



### 3.4 Visual summaries

The visualisation page focuses on giving quick, interpretable visuals for:
Gender distribution
Stroke vs non-stroke outcome
Age distribution
BMI distribution
Correlation heatmap for key numeric features
Charts are rendered with Matplotlib/Seaborn and saved to:
app/static/charts/
The templates then embed those static images into the dashboard.

### 3.5 Activity logging
To illustrate basic audit logging, the app writes a small record to MongoDB whenever certain events occur, such as:

Creating a patient
Updating a patient
Deleting a patient
Uploading a new dataset

Each entry captures:
Username
Action label (for example, CREATE_PATIENT)
A short detail string
Timestamp in UTC
These entries can be reviewed on an Activity Log page.

## 4. System layout
At a high level:
Flask app factory (create_hospital_app) wires everything together.
Blueprints split the functionality into auth, patient, and insights modules.
SQLite + SQLAlchemy manage user accounts.
MongoDB Atlas stores patient data and audit logs.
Pandas and Matplotlib generate tables and charts for analysis.

#### Directory overview
hospital_managment_application/
│
├── server.py                # Entry point – runs the Flask app
├── config.py                # Configuration helper
├── requirements.txt
├── .env                     # Environment variables (ignored by Git)
│
├── app/
│   ├── __init__.py          # create_hospital_app, blueprint registration
│   ├── extensions.py        # db, login_manager and other extensions
│   ├── models.py            # User model (SQLite)
│   ├── db_mongo.py          # MongoDB connection + helper functions
│   ├── security_utils.py    # Password hashing and related helpers
│   │
│   ├── auth/                # Login, register, profile
│   ├── patient/             # Patient CRUD
│   └── insights/            # Dashboard, data overview, visuals, activity log
│
├── app/templates/           # Jinja2 templates
└── app/static/              # CSS + generated chart images

## 5. Security and privacy checklist
This project is not a full security blueprint, but it deliberately includes several good practices:
    Passwords are hashed before storage (never plain text)
    CSRF tokens are included in forms (via Flask-WTF)
    Sensitive routes use @login_required
    Separate stores for user accounts (SQLite) and patient data (MongoDB)
    Config and secrets loaded from environment variables
    Audit log for important user actions
Real deployments in healthcare would also require:
    Transport encryption (HTTPS everywhere)
    Stronger access control and roles
    Formal data governance and regulatory compliance
    Robust logging, monitoring and incident response
Those are beyond the scope of this student project but are acknowledged in the documentation.

## 6. How to run the project
   
### 6.1 Environment setup
Create and activate a virtual environment:

python -m venv hospital_management
hospital_management\Scripts\activate
Install the dependencies:
pip install -r requirements.txt

### 6.2 Configuration
Create a .env file at the root of the project:
FLASK_SECRET_KEY=change-me
SQLITE_DB_URL=sqlite:///hospital_users.db

MongoDB Atlas URI – replace with your own details
MONGODB_URI=mongodb+srv://user:password@cluster-url/?retryWrites=true&w=majority
STROKE_DATA_PATH=dataset/healthcare-dataset-stroke-data.csv

Place the Kaggle stroke dataset CSV at:
dataset/healthcare-dataset-stroke-data.csv

### 6.3 Start the app
From the project root:
python server.py
Then open your browser at:
http://127.0.0.1:5000

You will be redirected to the login/register flow, and once logged in you can explore patients, data overview, visualisations and the activity log.

## 7. Tests
Pytest is configured through tests/conftest.py, which builds the app via create_hospital_app() and disables CSRF for test requests.
The current suite includes:
    test_auth_flow.py
        Verifies that the login and registration endpoints are reachable.
    test_patient_crud.py
        Verifies that /patients/ and /patients/add are not accessible to anonymous users and correctly redirect to the login page.
    test_data_insights.py
        Verifies that the home route / redirects to the login page when the user is not authenticated.
        Confirms that a data-related route (patients list) is also protected.

Run tests with:
pytest

All tests should pass (6 passed).

## 8. Possible next steps and extensions
Some obvious directions to extend this work:

Add role-based permissions (for example, admin vs standard user).
Export filtered patient data or analytics summaries as CSV/PDF.
Add simple predictive modelling (for example, train a small classifier on the stroke dataset and display risk scores).
Implement more detailed audit log filters and search.
Containerise the application with Docker and provide a one-command spin-up.

## 9. Note on AI assistance
AI tools were used during development to help with layout ideas and documentation drafts. All code has been manually integrated, checked and adapted to fit the module requirements and to ensure the final design decisions remain the responsibility of the author.

