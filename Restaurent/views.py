from django.shortcuts import render
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from .models import Menu, Customer, Order, Feedback, Employee, Lead
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

# creating user session
login_user = {}

def login(request):
    if request.method == 'POST':
        email1 = request.POST.get('email', '')
        password1 = request.POST.get('password', '')
        print(email1, password1)
        try:
            employee = Employee.objects.get(email=email1, password=password1)
            if employee.email == email1 and employee.password == password1:
                login_user['name'] = employee.name
                login_user['department'] = employee.department
                # return render(request, 'Dashboard.html')
                return dashboard(request)
            else:
                return render(request, 'login.html')
        except Exception as e:
            print("Enter valid email or password", e)
            messages.error(request, 'Please Enter Correct Username and Password!')


    return render(request, 'login.html')


def logout(request):
    del login_user['name']
    del login_user['department']

    return render(request, 'login.html')

def leadSource():
    l1 = Lead.objects.filter(lead_source='Swigy').count()
    l2 = Lead.objects.filter(lead_source='Zomato').count()
    lead_source_count = [l1, l2]
    lead_source_labels = ['Swiggy', 'Zomato']
    return lead_source_labels, lead_source_count


# @login_required(login_url='login')
def dashboard(request):

    if len(login_user) > 0:
        status_labels, status_values = customerStatus()
        # feedback = Feedback.objects.filter(feedback_date__month__gte=4)
        lead_source_labels, lead_source_count = leadSource()
        customer_loc_labels, customer_loc_values = customerLocation()
        total_customers = Customer.objects.all().count()
        total_leads = Lead.objects.all().count()
        orders = Order.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(
            c=Count("id")).values('month', 'c')  # filter by count of orders for current month

        today = date.today()
        a = today.month  # finding the current month using datetime
        orders_monthly = orders[a - 1]['c']  # filtering current month's order from dictionary

        earnings = Order.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(
            s=Sum("order_price")).values('month', 's')
        earnings_monthly = earnings[a - 1]['s']  # filtering current month's earnings from dictionary

        dish_orders = Order.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(
            c=F("menu")).values('month', 'c')  # filtering current month's dish count from dictionary
        # logic for monthly graphs
        earnings_values = []
        dish_orders_values = []

        for i in range(a):
            earnings_values.append(earnings[i]['s'])

        dish_wise_comparison_labels, dish_wise_comparison_values = logicFeedback(dish_orders)
        all_months = ['January', 'February', 'March', 'April', 'May']
        print(status_labels, status_values)
        context = {'total_customers': total_customers, 'earnings_monthly': earnings_monthly,
                   'total_orders': orders_monthly, 'all_months': all_months, 'earnings_values': earnings_values,
                   'dish_orders_values': dish_orders_values, 'total_leads': total_leads,
                   'dish_wise_comparison_labels': dish_wise_comparison_labels,
                   'dish_wise_comparison_values': dish_wise_comparison_values,
                   'lead_source_labels': lead_source_labels, 'lead_source_count': lead_source_count,
                   'customer_loc_labels': customer_loc_labels, 'customer_loc_values': customer_loc_values,
                   'status_labels': status_labels, 'status_values': status_values,
                   'user_name': login_user['name'], 'department': login_user['department']
                   }
        return render(request, 'Dashboard.html', context)
    else:
        return render(request, 'login.html')

def logicFeedback(dish_orders):
    import operator
    from _collections import OrderedDict
    dish_counts = []
    for j in range(len(dish_orders)):
        dish_counts.append(Menu.objects.get(id=dish_orders[j]['c']))
    dic = {}
    for k in range(len(dish_counts)):
        if dish_counts[k] in dic:
            dic[dish_counts[k]] += 1
        else:
            dic[dish_counts[k]] = 1

    dd = OrderedDict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
    dic_items = []
    # for i in range(5):
    #     dic_items.append((dd[i]).items())
    d1 = []
    d2 = []

    dic_items_keys = dd.keys()
    dic_items_values = dd.values()
    for o in range(5):
        d1.append(str(list(dic_items_keys)[o]))
        d2.append(str(list(dic_items_values)[o]))
    return d1, d2


def logic(feedback):
    d = {}
    # v = 0
    for i in range(len(feedback)):
        if feedback[i] in d:
            d[feedback[i]] += 1
        else:
            d[feedback[i]] = 1
    return d

def customerLocation():
    from _collections import OrderedDict
    customer = Customer.objects.annotate(month=TruncMonth('date_visited')).values('month').annotate(
        c=F("id")).values('month', 'c')
    # customer = Customer.objects.filter('')
    # print(list(customer))
    customerloc = []

    for i in range(len(customer)):
        customerid = customer[i]['c']
        customer_obj = Customer.objects.get(id=customerid)
        customerloc.append(customer_obj.customer_place)
    dic = {}
    for j in range(len(customerloc)):
        if customerloc[j] in dic:
            dic[customerloc[j]] += 1
        else:
            dic[customerloc[j]] = 1
    # print(dic)
    dd = OrderedDict(sorted(dic.items(), key=lambda x: x[1], reverse=True))

    d1 = []
    d2 = []

    dic_items_keys = dd.keys()
    dic_items_values = dd.values()
    for o in range(5):
        d1.append(list(dic_items_keys)[o])
        d2.append(list(dic_items_values)[o])
    return d1, d2


def customerStatus():
    from _collections import OrderedDict
    customer = Customer.objects.annotate(month=TruncMonth('date_visited')).values('month').annotate(
        c=F("id")).values('month', 'c')
    # customer = Customer.objects.filter('')
    # print(list(customer))
    customerstatus = []

    for i in range(len(customer)):
        customerid = customer[i]['c']
        customer_obj = Customer.objects.get(id=customerid)
        # print(customer_obj)
        customerstatus.append(str(customer_obj.status))
    # print(customerstatus)
    dic = {}
    for j in range(len(customerstatus)):
        if customerstatus[j] in dic:
            dic[customerstatus[j]] += 1
        else:
            dic[customerstatus[j]] = 1
    # print(dic)

    dic_items_keys = list(dic.keys())
    dic_items_values = list(dic.values())
    return dic_items_keys, dic_items_values


# def leadSource():
#     today = date.today()
#     a = today.month
#     lead = Lead.objects.values('date__year', 'date__month').annotate(count=Count('lead_source'))
#     return lead


def viewEmployee(request):
    if len(login_user) > 0:

        employee = Employee.objects.all()
        params = {'employee': employee, 'user_name': login_user['name'], 'department': login_user['department']}
        return render(request, 'ViewEmployee.html', params)
    else:
        return render(request, 'login.html')


def addEmployee(request):
    if len(login_user) > 0:

        params = {'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            name = request.POST.get('name', '')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            password1 = request.POST.get('password1', '')
            place = request.POST.get('place', '')
            department = request.POST.get('department', '')
            designation = request.POST.get('designation', '')
            date_joined = request.POST.get('date_joined', '')

            if password == password1:
                employee = Employee(name=name, phone=phone,
                                    email=email, password=password1,
                                    place=place,department=department, designation=designation, date_joined=date_joined
                                    )
                employee.save()
                messages.success(request, 'Employee added successfully!')
            else:
                print("Please enter the same password")
        return render(request, 'AddEmployee.html', params)
    else:
        return render(request, 'login.html')


def editEmployee(request, pk):
    if len(login_user) > 0:

        employees = Employee.objects.all()
        params = {'employee': employees}
        employee = Employee.objects.get(id=pk)
        context = {'employee': employee, 'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            employee.name = request.POST.get('name', '')
            employee.phone = request.POST.get('phone', '')
            employee.place = request.POST.get('place', '')
            employee.department = request.POST.get('department', '')
            employee.email = request.POST.get('email', '')
            employee.password = request.POST.get('password1', '')
            employee.designation = request.POST.get('designation', '')
            employee.date_joined = request.POST.get('date_joined', '')
            # employee.date_visited = datetime.datetime.now()
            employee.save()
            messages.success(request, 'Employee updated successfully!')
            return render(request, 'ViewEmployee.html', params)

        return render(request, 'UpdateEmployee.html', context)
    else:
        return render(request, 'login.html')


def deleteEmployee(request, pk):
    # print("deleting")
    employee_obj = Employee.objects.get(id=pk)
    employee_obj.delete()
    employee = Employee.objects.all()
    params = {'employee': employee, 'user_name': login_user['name'], 'department': login_user['department']}
    messages.success(request, 'Employee deleted successfully!')
    return render(request, 'ViewEmployee.html', params)


def viewFeedback(request):
    if len(login_user) > 0:

        feedback = Feedback.objects.all()
        params = {'feedback': feedback, 'user_name': login_user['name'], 'department': login_user['department']}
        return render(request, 'ViewFeedback.html', params)
    else:
        return render(request, 'login.html')


def addFeedback(request):
    if len(login_user) > 0:

        customers = Customer.objects.all()
        menus = Menu.objects.all()
        params = {'customer': customers, 'menu': menus, 'user_name': login_user['name'], 'department': login_user['department']}

        if request.method == 'POST':
            # print("I am for loop", request.POST.get("customer_phone"))
            customer_name_feedback = request.POST.get('customer_name_feedback', '')
            customer_phone = request.POST.get('customer_phone', '')
            customer_age = request.POST.get('customer_age', '')
            customer_gender = request.POST.get('customer_gender', '')
            dish_name = request.POST.get('dish_name', '')
            rating = request.POST.get('rating', '')
            review = request.POST.get('review', '')
            feedback_date = request.POST.get('feedback_date', '')
            dish_id = Menu.objects.get(id=dish_name)
            customer_id = Customer.objects.get(id=customer_phone)
            print("Phone", customer_phone)
            feedback = Feedback(customer=customer_id, menu=dish_id,
                                customer_name_feedback=customer_name_feedback,
                                customer_age=customer_age, customer_gender=customer_gender,
                                rating=rating, review=review, feedback_date=feedback_date
                                )
            feedback.save()
            messages.success(request, 'Feedback added successfully!')
        return render(request, 'AddFeedback.html', params)
    else:
        return render(request, 'login.html')


def deleteFeedback(request, pk):
    feedback_obj = Feedback.objects.get(id=pk)
    feedback_obj.delete()
    feedback = Feedback.objects.all()
    params = {'feedback': feedback, 'user_name': login_user['name'], 'department': login_user['department']}
    messages.success(request, 'Feedback deleted successfully!')
    return render(request, 'ViewFeedback.html', params)


def viewCustomer(request):
    if len(login_user) > 0:

        customer = Customer.objects.all()
        params = {'customer': customer, 'user_name': login_user['name'], 'department': login_user['department']}
        return render(request, 'ViewCustomer.html', params)
    else:
        return render(request, 'login.html')


def addCustomer(request):
    if len(login_user) > 0:

        params = {'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            customer_name = request.POST.get('customer_name', '')
            customer_phone = request.POST.get('customer_phone', '')
            customer_email = request.POST.get('customer_email', '')
            customer_place = request.POST.get('customer_place', '')
            date_visited = request.POST.get('date_visited', '')
            status = request.POST.get('status', '')

            customer = Customer(customer_name=customer_name, customer_phone=customer_phone,
                                customer_email=customer_email, customer_place=customer_place,
                                date_visited=date_visited, status=status
                                )
            customer.save()
            messages.success(request, 'Customer added successfully!')
        return render(request, 'AddCustomer.html', params)
    else:
        return render(request, 'login.html')


def editCustomer(request, pk):
    if len(login_user) > 0:

        customers = Customer.objects.all()
        params = {'customer': customers, 'user_name': login_user['name'], 'department': login_user['department']}
        customer = Customer.objects.get(id=pk)
        context = {'customer': customer, 'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            customer.customer_name = request.POST.get('customer_name', '')
            customer.customer_phone = request.POST.get('customer_phone', '')
            customer.customer_email = request.POST.get('customer_email', '')
            customer.customer_place = request.POST.get('customer_place', '')
            customer.date_visited = date.today()
            # customer = Customer(customer_name=customer_name, customer_phone=customer_phone,
            #                     customer_email=customer_email, customer_place=customer_place, date_visited=date_visited
            #                     )
            customer.save()
            messages.success(request, 'Customer updated successfully!')
            return render(request, 'ViewCustomer.html', params)
        return render(request, 'UpdateCustomer.html', context)
    else:
        return render(request, 'login.html')


def deleteCustomer(request, pk):
    # print("deleting")
    customer_obj = Customer.objects.get(id=pk)
    customer_obj.delete()
    customer = Customer.objects.all()
    params = {'customer': customer, 'user_name': login_user['name'], 'department': login_user['department']}
    messages.success(request, 'Customer deleted successfully!')
    return render(request, 'ViewCustomer.html', params)



def viewMenu(request):
    if len(login_user) > 0:

        menus = Menu.objects.all()
        params = {'menu': menus, 'user_name': login_user['name'], 'department': login_user['department']}

        return render(request, 'ViewMenu.html', params)
    else:
        return render(request, 'login.html')


def addMenu(request):
    if len(login_user) > 0:

        param = {'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            dish_category = request.POST.get('dish_category', '')
            dish_name = request.POST.get('dish_name', '')
            dish_price = request.POST.get('dish_price', '')
            menu = Menu(dish_category=dish_category, dish_name=dish_name, dish_price=dish_price)
            menu.save()
            messages.success(request, 'Menu added successfully!')
        return render(request, 'AddMenu.html', param)
    else:
        return render(request, 'login.html')


def editMenu(request, pk):
    if len(login_user) > 0:

        menu = Menu.objects.all()
        params = {'menu': menu, 'user_name': login_user['name'], 'department': login_user['department']}
        menu_obj = Menu.objects.get(id=pk)
        context = {'menu_obj': menu_obj, 'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            menu_obj.dish_category = request.POST.get('dish_category', '')
            menu_obj.dish_name = request.POST.get('dish_name', '')
            menu_obj.dish_price = request.POST.get('dish_price', '')

            menu_obj.save()
            messages.success(request, 'Menu updated successfully!')
            return render(request, 'ViewMenu.html', params)
        return render(request, 'UpdateMenu.html', context)
    else:
        return render(request, 'login.html')


def deleteMenu(request, pk):
    if len(login_user):

        # print("deleting")
        menu_obj = Menu.objects.get(id=pk)
        menu_obj.delete()
        menu = Menu.objects.all()
        params = {'menu': menu, 'user_name': login_user['name'], 'department': login_user['department']}
        messages.success(request, 'Menu deleted successfully!')
        return render(request, 'ViewMenu.html', params)
    else:
        return render(request, 'login.html')


def viewOrder(request):
    if len(login_user) > 0:

        order = Order.objects.all()
        params = {'order': order, 'user_name': login_user['name'], 'department': login_user['department']}
        return render(request, 'ViewOrder.html', params)
    else:
        return render(request, 'login.html')


def addOrder(request):
    if len(login_user) > 0:

        customers = Customer.objects.all()
        menus = Menu.objects.all()
        params = {'customer': customers, 'menu': menus, 'user_name': login_user['name'], 'department': login_user['department']}

        if request.method == 'POST':
            # print("I am for loop", request.POST.get("customer_phone"))
            customer_phone = request.POST.get('customer_phone', '')
            customer_name_order = request.POST.get('customer_name_order', '')
            dish_name = request.POST.get('dish_name', '')
            order_quantity = request.POST.get('order_quantity', '')
            order_price = request.POST.get('order_price', '')
            order_date = request.POST.get('order_date', '')
            dish_id = Menu.objects.get(id=dish_name)
            customer_id = Customer.objects.get(id=customer_phone)
            print("Phone", order_price)
            order = Order(customer=customer_id, menu=dish_id, customer_name_order=customer_name_order,
                          order_quantity=order_quantity, order_price=order_price, order_date=order_date
                          )
            order.save()
            messages.success(request, 'Order added successfully!')
        return render(request, 'AddOrder.html', params)
    else:
        return render(request, 'login.html')


def editOrder(request, pk):
    if len(login_user) > 0:

        customer = Customer.objects.all()
        menu = Menu.objects.all()
        order = Order.objects.all()
        params = {'order': order, 'customer': customer, 'menu': menu, 'user_name': login_user['name'], 'department': login_user['department']}
        order_pk = Order.objects.get(id=pk)
        context = {'order_pk': order_pk, 'menu': menu, 'customer': customer, 'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            order_pk.customer_name_order = request.POST.get('customer_name_order', '')
            order_pk.customer_phone = request.POST.get('customer_phone', '')
            order_pk.dish_name = request.POST.get('dish_name', '')
            order_pk.order_quantity = request.POST.get('order_quantity', '')
            order_pk.order_price = request.POST.get('order_price', '')
            order_pk.order_date = request.POST.get('order_date', '')

            order_pk.save()
            messages.success(request, 'Order updated successfully!')
            return render(request, 'ViewOrder.html', params)
        return render(request, 'UpdateOrder.html', context)
    else:
        return render(request, 'login.html')


def deleteOrder(request, pk):
    # print("deleting")
    order_obj = Order.objects.get(id=pk)
    order_obj.delete()
    order = Order.objects.all()
    params = {'order': order, 'user_name': login_user['name'], 'department': login_user['department']}
    messages.success(request, 'Order deleted successfully!')
    return render(request, 'ViewOrder.html', params)


def viewLead(request):
    if len(login_user) > 0:

        lead = Lead.objects.all()
        params = {'lead': lead, 'user_name': login_user['name'], 'department': login_user['department']}
        return render(request, 'ViewLead.html', params)
    else:
        return render(request, 'login.html')


def addLead(request):
    if len(login_user) > 0:

        param = {'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            lead_name = request.POST.get('lead_name', '')
            lead_email = request.POST.get('lead_email', '')
            lead_source = request.POST.get('lead_source', '')
            lead_phone = request.POST.get('lead_phone', '')
            lead_location = request.POST.get('lead_location', '')
            lead = Lead(lead_name=lead_name, lead_source=lead_source, lead_email=lead_email, lead_phone=lead_phone,
                        lead_location=lead_location)
            lead.save()
            messages.success(request, 'Lead added successfully!')
        return render(request, 'AddLeads.html', param)
    else:
        return render(request, 'login.html')


def editLead(request, pk):
    if len(login_user) > 0:

        lead = Lead.objects.all()
        params = {'lead': lead, 'user_name': login_user['name'], 'department': login_user['department']}
        edit_lead = Lead.objects.get(id = pk)
        context = {'leads': edit_lead, 'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            edit_lead.lead_name = request.POST.get('lead_name', '')
            edit_lead.lead_email = request.POST.get('lead_email', '')
            edit_lead.lead_source = request.POST.get('lead_source', '')
            edit_lead.lead_phone = request.POST.get('lead_phone', '')
            edit_lead.lead_location = request.POST.get('lead_location', '')

            edit_lead.save()
            messages.success(request, 'Lead updated successfully!')
            return render(request, 'ViewLead.html', params)

        return render(request, 'UpdateLead.html', context)
    else:
        return render(request, 'login.html')



def deleteLead(request, pk):
    if len(login_user) > 0:

        lead = Lead.objects.all()
        params = {'lead': lead, 'user_name': login_user['name'], 'department': login_user['department']}
        # print("deleting")
        lead = Lead.objects.get(id=pk)
        lead.delete()
        messages.success(request, 'Lead deleted successfully!')

        return render(request, 'ViewLead.html', params)
    else:
        return render(request, 'login.html')











def composeMail(request):
    if len(login_user) > 0:

        params = {'user_name': login_user['name'], 'department': login_user['department']}
        if request.method == 'POST':
            email = request.POST.get('mail_id', '')
            mail_subject = request.POST.get('mail_subject', '')
            mail_body = request.POST.get('mail_body', '')

            send_mail(mail_subject, mail_body, settings.EMAIL_HOST_USER, [str(email)],
                      fail_silently=False)
            messages.success(request, 'Mail Send successfully!')
        return render(request, 'ComposeMail.html', params)
    else:
        return render(request, 'login.html')

# def addMenuRequest(request):
#     if request.method == 'POST':
#         dish_category = request.POST.get('dish_category')
#         dish_name = request.POST.get('dish_name')
#         dish_price = request.POST.get('dish_price')
#         menu = Menu(dish_category=dish_category, dish_name=dish_name, dish_price=dish_price)
#         menu.save()
#
#         return render(request, 'AddMenu.html')
