# Expense_Split_App

# Expenses Sharing App

**Overview**
The Expenses Sharing App is a simple Django web application that allows users to split shared expenses. The app supports user authentication, expense tracking, and the ability to download balance sheets. Users can view who owes money and who they owe money to. It also supports different methods for splitting expenses: equal, percentage-based, or exact amounts.

**Features**
* User registration and login
* Add shared expenses between users
* Split expenses equally, by percentage, or by exact amounts
* View balances for each user
* Download a balance sheet as a CSV file
  
**Prerequisites**
Make sure you have the following installed on your machine:

Python 3.6+: Download here
pip: Python's package installer, typically installed with Python.
Virtual environment (optional but recommended): You can use venv to create an isolated environment for this project.
Setup Instructions

Follow these steps to get the project running locally.

# 1. Clone the Repository
First, clone the repository to your local machine using the following command:

bash
Copy code
git clone https://github.com/Sandhya0224/Expense_Split_App.git
cd Expenses_Sharing_App

# 2. Create and Activate a Virtual Environment (Optional but Recommended)
To avoid package conflicts, it's recommended to create a virtual environment for the project.

bash
Copy code
# On Windows
python -m venv env
env\Scripts\activate

# On macOS/Linux
python3 -m venv env
source env/bin/activate

# 3. Install Dependencies
Once you're inside the project directory, install all the required packages using pip.

bash
Copy code
pip install django
Optionally, if there is a requirements.txt file in the project, you can install all dependencies at once:

bash
Copy code
pip install -r requirements.txt

# 4. Apply Migrations
The project uses a SQLite database by default. Run the following command to apply all necessary database migrations:

bash
Copy code
python manage.py migrate

# 5. Create a Superuser (Admin Access)
To access the Django admin panel, you’ll need to create a superuser:

bash
Copy code
python manage.py createsuperuser
Follow the prompts to create an admin account with a username, email, and password.

# 6. Run the Server
Start the Django development server with this command:

bash
Copy code
python manage.py runserver

Once the server is running, open your browser and navigate to:
Copy code
http://127.0.0.1:8000/
You should see the Expenses Sharing App running locally.

# 7. Access the Admin Panel
To manage the app's data through the admin interface, go to:

Copy code
http://127.0.0.1:8000/admin/
Log in using the superuser credentials you created earlier.

**App Features and API Endpoints**
User Registration and Login
You can use the following endpoints to register and log in users:

# Register a New User (POST): /account/create_user/

Request Body:
json
Copy code
{
    "username": "john_doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "password": "password123"
}

# Login (POST): /account/login_user/

Request Body:
json
Copy code
{
    "username": "john_doe",
    "password": "password123"
}

**Add Expense**
To add an expense and split it among users, you can use the following endpoint:

# Add Expense (POST): /add_expense/
Request Body:
json
Copy code
{
    "current_id": 1,
    "amount": 100,
    "split_type": "equal",  # or 'percentage', 'exact'
    "split_details": [{"id": 2}, {"id": 3}]
}

**View Overall User Expenses**

# View All Users' Expenses (GET): /users_expenses/

Displays the total outgoing, incoming, and net balance for all users.
Download Balance Sheet

# Download a CSV of the Balance Sheet (GET): /download_balance_sheet/
Project Structure
Here's a basic outline of the project structure:

Expenses_Sharing_App/
│
├── account/                # Handles user authentication and account management
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── Expenses_app/           # Handles expense management
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
│
├── Expenses_Sharing_App/   # Project-level configurations
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3              # SQLite database file
├── manage.py               # Django's CLI entry point
└── requirements.txt        # Dependencies list (if created)
