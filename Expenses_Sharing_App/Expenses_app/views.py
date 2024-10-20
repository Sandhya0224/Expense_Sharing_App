from django.http import JsonResponse, HttpResponse
from .models import Expense
from account.models import CustomUser
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json, csv

# Create your views here.

# 1. Retrieve user details
# @login_required  
def user_details(request):

    user = request.user   #current user from request body
    user_details = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
    }
    return JsonResponse(user_details)

# Returns list of users
@require_http_methods(["GET"])
def list_user_details(request):

    users = CustomUser.objects.all()
    user_details = []
    for user in users:
        user_info = {
            'username': user.username,
            'email': user.email,
            'phone': user.phone
        }
        user_details.append(user_info)
    return JsonResponse({'users': user_details}, safe=False)


# 2. a) Get all the split details that the current user need to pay
@require_http_methods(["GET"])
def splitpay_to_id(request, id, *args, **kwargs):

    expenses = Expense.objects.filter(to_id=id, status=False)
    user_name = []
    user_amt = []

    for expense in expenses:
        try:
            # Get the user who owes the money (from_id)
            user = CustomUser.objects.get(id=expense.from_id)
            user_name.append(user.username)
            user_amt.append(expense.amount)

        except CustomUser.DoesNotExist:
            user_name.append('Unknown User')
            user_amt.append(0)
        # mapping usernames to the amount they owe
    user_info = dict(zip(user_name, user_amt))

    return JsonResponse(user_info)

# b) get all the users who has to pay split amount to current user
@require_http_methods(["GET"])
def splitpay_from_id(request, id, *args, **kwargs):
    expenses = Expense.objects.filter(from_id=id, status=False)
    user_name = []
    user_amt = []

    for expense in expenses:
        try:
            # Get the user who is owed money (
            user = CustomUser.objects.get(id=expense.to_id)
            user_name.append(user.username)
            user_amt.append(expense.amount)

        except CustomUser.DoesNotExist:
            user_name.append('Unknown User')
            user_amt.append(0)

    # mapping usernames to the amount they are owed
    user_info = dict(zip(user_name, user_amt))

    return JsonResponse(user_info)

# 3. Add expense
@csrf_exempt
def add_expense(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # accessing data from request body
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        current_id = data.get('current_id')
        total_amount = data.get('amount')
        split_type = data.get('split_type')  
        split_details = data.get('split_details')  

        if not current_id or total_amount is None or not split_type or not split_details:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Process splits based on the aplit type
        expenses_to_add = []

        for detail in split_details:
            to_id = detail.get('id')
            if split_type == 'equal':
                # Equal split
                split_amount = total_amount / len(split_details)
                expenses_to_add.append((current_id, to_id, split_amount))

            elif split_type == 'percentage':
                # Percentage split
                percentage = detail.get('percentage')

                if percentage is None or percentage < 0 or percentage > 100:
                    return JsonResponse({'error': 'Invalid percentage value'}, status=400)
                split_amount = (percentage / 100) * total_amount
                expenses_to_add.append((current_id, to_id, split_amount))

            elif split_type == 'exact':
                # Exact amount split
                split_amount = detail.get('split_amount')

                if split_amount is None or split_amount < 0 or split_amount > total_amount:
                    return JsonResponse({'error': 'Invalid split amount'}, status=400)
                expenses_to_add.append((current_id, to_id, split_amount))

            else:
                return JsonResponse({'error': 'Invalid split type'}, status=400)

        # Add data to Expense table
        for from_id, to_id, amount in expenses_to_add:
            Expense.objects.create(from_id=from_id, to_id=to_id, amount=amount)

        return JsonResponse({'message': 'Expenses created successfully'}, status=201)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


# 4. Retrieve overall expenses
@csrf_exempt
def get_all_user_expenses(request):
    if request.method == 'GET':
        try:
            users = CustomUser.objects.all()
            overall_expenses = []

            for user in users:
                # Calculate total expenses for each user
                total_expenses_outgoing = Expense.objects.filter(from_id=user.id).aggregate(total=Sum('amount'))['total'] or 0
                total_expenses_incoming = Expense.objects.filter(to_id=user.id).aggregate(total=Sum('amount'))['total'] or 0
                
                overall_expense = {
                    'username': user.username,
                    'total_outgoing': str(total_expenses_outgoing), 
                    'total_incoming': str(total_expenses_incoming),  
                    'net_expenses': str(total_expenses_outgoing - total_expenses_incoming)  
                }

                overall_expenses.append(overall_expense)

            response_data = {
                'overall_expenses': overall_expenses
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


# 6. Download balancesheet
def download_balance_sheet(request):
    if request.method == 'GET':
        # Create the HTTP response with CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

        # Create CSV writer object
        writer = csv.writer(response)
        
        writer.writerow(['Username', 'Total Outgoing', 'Total Incoming', 'Net Balance'])
        users = CustomUser.objects.all()

        for user in users:
            total_outgoing = Expense.objects.filter(from_id=user.id).aggregate(total=Sum('amount'))['total'] or 0
            total_incoming = Expense.objects.filter(to_id=user.id).aggregate(total=Sum('amount'))['total'] or 0
            net_balance = total_incoming - total_outgoing
            
            # Write the user's balance data to the CSV
            writer.writerow([
                user.username.strip(),  
                f"      {total_outgoing:}       ",  
                f"      {total_incoming:}       ",  
                f"      {net_balance:}      "     
            ])

        return response
    return HttpResponse('Invalid request method', status=405)



