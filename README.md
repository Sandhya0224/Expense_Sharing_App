# Expenses Sharing App
A Django-based web application that allows users to track, split, and manage shared expenses. Users can add expenses, see who owes what, and download the balance sheet for all transactions.

# Table of Contents
[Features]
[Installation]
[Running the Application]
[API Endpoints]

# Features
User registration and authentication (user accounts are created via an admin interface).
Add and split expenses between users based on equal shares, percentages, or exact amounts.
Retrieve all expenses a user owes or is owed.
Download a balance sheet (CSV file) summarizing total balances.
Track overall expenses for all users, including net balances.

# Installation
**1. Clone the Repository**
bash
Copy code
git clone <repository_url>
cd Expenses_Sharing_App

**2. Create a Virtual Environment (Optional but recommended)**
bash
Copy code
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

**3. Install Dependencies**
bash
Copy code
pip install django

**4. Apply Migrations**
bash
Copy code
python manage.py migrate

**5. Create a Superuser (Admin)**
bash
Copy code
python manage.py createsuperuser

**6. Run the Server**
bash
Copy code
python manage.py runserver

Running the Application
Once the server is running, open your browser and navigate to:

Admin Panel: [http://127.0.0.1:8000/admin]

Login using the superuser credentials created earlier.
To stop the server, press Ctrl + C.

# API Endpoints
Here are all the available API routes in the application:

**1. Account Routes (User Management)**
Create User (via Admin)
URL: /admin/
Method: N/A
Description: Create users and manage accounts using Django’s built-in admin interface.

**2. Expense Routes**

Retrieve User Details (Current User)

URL: /user_details/
Method: GET
Description: Returns the details of the current authenticated user.
Response:
json
Copy code
{
   "id": 1,
   "username": "john_doe",
   "email": "john@example.com",
   "phone": "1234567890"
}

List All Users

URL: /list_user_details/
Method: GET
Description: Returns a list of all registered users.
Response:
json
Copy code
{
   "users": [
      {
         "username": "john_doe",
         "email": "john@example.com",
         "phone": "1234567890"
      },
      {
         "username": "jane_doe",
         "email": "jane@example.com",
         "phone": "0987654321"
      }
   ]
}

Add Expense

URL: /add_expense/
Method: POST
Description: Adds a new expense and splits it among users.
Request Body:
json
Copy code
{
   "current_id": 1,
   "amount": 100,
   "split_type": "equal",  # 'equal', 'percentage', 'exact'
   "split_details": [
       {"id": 2}, 
       {"id": 3}
   ]
}

Split by percentage:

json
Copy code
{
   "current_id": 1,
   "amount": 100,
   "split_type": "percentage",
   "split_details": [
       {"id": 2, "percentage": 60}, 
       {"id": 3, "percentage": 40}
   ]
}

Split by exact amount:

json
Copy code
{
   "current_id": 1,
   "amount": 100,
   "split_type": "exact",
   "split_details": [
       {"id": 2, "split_amount": 60}, 
       {"id": 3, "split_amount": 40}
   ]
}

Expenses Owed to User
URL: /split_to_be_paid/<int:id>/
Method: GET
Description: Retrieves all unpaid expenses owed to the user with id.

Expenses Owed by User
URL: /split_to_pay/<int:id>/
Method: GET
Description: Retrieves all unpaid expenses that the user with id owes to others.

Overall Expenses
URL: /users_expenses/
Method: GET
Description: Retrieves total outgoing and incoming expenses for each user, along with their net balances.
Response:
json
Copy code
{
   "overall_expenses": [
      {
         "username": "john_doe",
         "total_outgoing": "150.00",
         "total_incoming": "100.00",
         "net_expenses": "50.00"
      },
      {
         "username": "jane_doe",
         "total_outgoing": "80.00",
         "total_incoming": "120.00",
         "net_expenses": "-40.00"
      }
   ]
}

Download Balance Sheet
URL: /download_balance_sheet/
Method: GET
Description: Downloads a CSV file containing all users' outgoing, incoming, and net balances.

File Example:
csv
Copy code
Username, Total Outgoing, Total Incoming, Net Balance
john_doe, 150.00, 100.00, 50.00
jane_doe, 80.00, 120.00, -40.00
