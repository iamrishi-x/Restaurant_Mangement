from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Dish,DefaultDish,Customer,Customer_Dish,RoomTable,TableInfo
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import datetime,timedelta
import json

@login_required
def Table_View(request):
    all_roomTables = RoomTable.objects.all()
    table_info = TableInfo.objects.filter(is_close=1)
    table_info_left = TableInfo.objects.all()
    # print(all_roomTables)
    if request.method == 'POST' and request.POST['Custname']!='':

        print('#' * 50)
        print(request.POST)
        now = datetime.now() + timedelta(hours=5,minutes=30)
        current_time = now.strftime("%H:%M:%S")

        #Customer model Attributes
        name = request.POST['Custname']
        phone = request.POST['CustPhone']
        address = request.POST['CustAddress']
        date = request.POST['CustorderDate']
        payment_option = request.POST['Custpayment_option']
        order_type = request.POST['CustOrder_type']  # Dine In / Take Away
        order_status = 'Waiting'
        order_total = 0
        no_of_people = request.POST['CustTotalFamilyMember']
        table = request.POST['CustTable']
        cust_obj = Customer(name=name,phone=phone,address=address,date=date,time_in=current_time,payment_option=payment_option,order_type=order_type,order_status=order_status,order_total=order_total,no_of_people=no_of_people,table=table)
        cust_obj.save()
        #Table info
        print(cust_obj.table)
        try:
            table = TableInfo.objects.get(table_n=cust_obj.table)
        except:
            return render(request, 'CustomerAndDish/index_table.html',{'all_roomTables': all_roomTables, 'table_info': table_info,'table_info_left': table_info_left},messages.error(request, 'First Submit Table Layout ! Go To Table Layout Setting -> Submit Layout', 'alert-danger'))
        # table.in_time = current_time
        table.is_close = 1
        table.cust_id = cust_obj
        table.save()
        # print(table.in_time)
        # table.in_time += timedelta(hours=5,minutes=30)
        # table.save()
        # print(table.in_time)
        table = cust_obj.table
        print(table)
        return redirect('newOrder', table)
    return render(request, 'CustomerAndDish/index_table.html', {'all_roomTables': all_roomTables,'table_info': table_info,'table_info_left':table_info_left})

@login_required
def All_Order(request):
    orders = Customer.objects.all()
    return render(request,'CustomerAndDish/index_orders.html',{'orders': orders})

@login_required
def AddDish(request,table):
    print('-----------------------------------In Add Dish-----------------------------------')
    if request.POST['oper'] == 'Delete Dish Row':
        table_name = request.POST['table_id']
        table_obj = TableInfo.objects.get(table_n=table_name)
        cust_id = table_obj.cust_id
        dish_name = request.POST['dish_name']
        dish_id = Dish.objects.get(dish_name=dish_name)
        cust_dish_obj = Customer_Dish.objects.get(cust_id=cust_id, dish_id=dish_id)

        Dishes = Dish.objects.filter(active=1)
        table_obj = TableInfo.objects.get(table_n=table_name)
        if cust_dish_obj.delete():
            dishes_object = Customer_Dish.objects.filter(cust_id=cust_id)
            return render(request, 'CustomerAndDish/new_order.html',{'Dishes': Dishes, 'table_obj': table_obj, 'order_dises': dishes_object})
        else:
            dishes_object = Customer_Dish.objects.filter(cust_id=cust_id)
            return render(request, 'CustomerAndDish/new_order.html',{'Dishes': Dishes, 'table_obj': table_obj, 'order_dises': dishes_object})

    if request.POST['oper'] == 'UpdateDataAll':
        table_name = request.POST['table_id']
        table_obj = TableInfo.objects.get(table_n=table_name)
        cust_id = table_obj.cust_id
        data_dishid = json.loads(request.POST['data_dishid'])
        print(data_dishid)
        data_dishPrice = json.loads(request.POST['data_dishPrice'])
        print(data_dishPrice)
        data_quantity = json.loads(request.POST['data_quantity'])
        print(data_quantity)
        data_rowPrice = json.loads(request.POST['data_rowPrice'])
        print(data_rowPrice)
        for i,j,k,l in zip(data_dishid,data_dishPrice,data_quantity,data_rowPrice):
            print(i)
            dish_id = Dish.objects.get(dish_name=i)
            cust_dish_obj = Customer_Dish.objects.get(cust_id=cust_id, dish_id=dish_id)
            cust_dish_obj.dish_price = int(j)
            cust_dish_obj.quantity = int(k)
            cust_dish_obj.dish_row_total = int(l)
            cust_dish_obj.save()
        #Basic Sending data
        Dishes = Dish.objects.filter(active=1)
        table_obj = TableInfo.objects.get(table_n=table_name)
        dishes_object = Customer_Dish.objects.filter(cust_id=cust_id)
        return render(request, 'CustomerAndDish/new_order.html',{'Dishes': Dishes, 'table_obj': table_obj, 'order_dises': dishes_object})
    else:
        print(request.POST)
        dish_name = request.POST['dish_name']
        dish_id = Dish.objects.get(dish_name=dish_name)
        # dish_id.active = 0
        # dish_id.save()
        Dishes = Dish.objects.filter(active=1)
        quantity = request.POST['dish_quantity']
        dish_price = request.POST['dish_cost']
        table_name = request.POST['table_id']
        table_obj = TableInfo.objects.get(table_n=table_name)
        cust_id = table_obj.cust_id
        if request.POST['oper'] == 'EditData':
            cust_dish_obj = Customer_Dish.objects.get(cust_id=cust_id, dish_id=dish_id)
            cust_dish_obj.quantity = quantity
            cust_dish_obj.dish_row_total = int(quantity)*int(dish_price)
        elif request.POST['oper'] == 'AddData':
            try:
                cust_dish_obj = Customer_Dish.objects.get(cust_id=cust_id, dish_id=dish_id)
                cust_dish_obj.quantity = int(cust_dish_obj.quantity) + int(quantity)
                cust_dish_obj.dish_row_total = int(cust_dish_obj.quantity) * int(dish_price)
                cust_dish_obj.save()
            except:
                cust_dish_obj = Customer_Dish(cust_id=cust_id, dish_id=dish_id, dish_price=dish_price, quantity=quantity,dish_row_total=(int(dish_price) * int(quantity)))
                cust_dish_obj.save()
        dishes_object = Customer_Dish.objects.filter(cust_id=cust_id)
        print('*' * 40)
        print(dishes_object)
        # print()
        # order_dises = zip(len(list(dishes_object)), dishes_object)
        return render(request, 'CustomerAndDish/new_order.html',{'Dishes': Dishes, 'table_obj': table_obj, 'order_dises': dishes_object})

@login_required
def New_Order(request,table):  #After table click New
    print('-' * 30 + 'New Order' + '-' * 30)
    table_obj = TableInfo.objects.get(table_n=table)
    cust_id = table_obj.cust_id
    dishes_object = Customer_Dish.objects.filter(cust_id=cust_id)
    grand_total = 0
    for i in dishes_object:
        grand_total+=i.dish_price * i.quantity
    cust_id.order_total = grand_total
    cust_id.save()
    Dishes = Dish.objects.filter(active=1)
    if request.POST:
        cust_obj = table_obj.cust_id
        name = request.POST['Custname']
        cust_obj.name = name
        phone = request.POST['CustPhone']
        cust_obj.phone = phone
        address = request.POST['CustAddress']
        cust_obj.address = address
        # payment_option = request.POST['Custpayment_option']
        payment_option = 'Postpay'
        cust_obj.payment_option = payment_option
        order_type = 'Dine In' # Dine In / Take Away
        cust_obj.order_type = order_type
        no_of_people = request.POST['CustTotalFamilyMember']
        cust_obj.no_of_people = no_of_people
        order_status = request.POST['Orderstate']
        cust_obj.order_status = order_status
        if order_status == 'Paid':
            table_obj.is_close = 0
            table_obj.save()
        dishes_object = Customer_Dish.objects.filter(cust_id=cust_id)
        grand_total = 0
        for i in dishes_object:
            grand_total += i.dish_price * i.quantity
        cust_obj.order_total = grand_total

        cust_obj.save()
        return render(request, 'CustomerAndDish/new_order.html', {'Dishes': Dishes,'table_obj':table_obj, 'order_dises': dishes_object},messages.success(request, 'Customer Info Edited successfully !', 'alert-success'))
    return render(request, 'CustomerAndDish/new_order.html',{'Dishes': Dishes, 'table_obj': table_obj, 'order_dises': dishes_object})

@login_required
def Print_Order(request,cust_id):
    cust_dishes = Customer_Dish.objects.filter(cust_id=cust_id)
    customer = Customer.objects.get(cust_id=cust_id)
    # print(customer.table)
    table_obj = TableInfo.objects.get(table_n=customer.table)
    # if table_obj.cust_id.order_status == 'Paid':
    customer.order_status = 'Paid'
    table_obj.is_close = 0
    customer.save()
    table_obj.save()
    return render(request,'CustomerAndDish/print_order.html', {'cust_dishes':cust_dishes, 'customer':customer})

@login_required
def Edit_Order(request,cust_id):
    customer = Customer.objects.get(cust_id=cust_id)
    table_obj = TableInfo.objects.get(table_n=customer.table)
    dishes_object = Customer_Dish.objects.filter(cust_id=cust_id)
    Dishes = Dish.objects.all()
    return render(request, 'CustomerAndDish/new_order.html', {'Dishes': Dishes,'table_obj':table_obj, 'order_dises': dishes_object})

@login_required
def Delete_Order(request,cust_id):
    customer = Customer.objects.get(cust_id=cust_id)
    table_obj = TableInfo.objects.get(table_n=customer.table)
    table_obj.is_close = 0
    table_obj.save()
    if customer.delete():
        return redirect('/CustomerAndDish/', messages.success(request, 'Order was successfully deleted.', 'alert-success'))
    else:
        return redirect('/CustomerAndDish/', messages.error(request, 'Cannot delete Order.', 'alert-danger'))

@login_required
def All_Dish(request):
    dishes = Dish.objects.all()
    return render(request, 'CustomerAndDish/index_dishes.html', {'dishes': dishes})

@login_required
def New_Dish(request):
    Dishes = DefaultDish.objects.filter(active = 1)
    if request.POST:
        new_Dish = request.POST['new_Dish']   #-------1
        def_dish_obj = DefaultDish.objects.get(dish_name_Def=new_Dish)  #-------2
        def_dish_obj.active = 0
        dish_name = new_Dish   #-------3
        if request.POST['new_Category'] == 'None':#-------4
            category = def_dish_obj.category
        else:
            category = request.POST['new_Category']
        if request.POST['new_SubCategory'] == 'None':  #-------5
            subcategory = def_dish_obj.subcategory
        else:
            subcategory = request.POST['new_SubCategory']
        active = request.POST['new_Active']
        price = request.POST['new_DishPrice']
        dish_obj = Dish(def_dish_id = def_dish_obj , dish_name = dish_name , category = category ,subcategory = subcategory , active =active,price=price)
        def_dish_obj.save()
        dish_obj.save()
        Dishes = DefaultDish.objects.filter(active=1)
    return render(request, 'CustomerAndDish/new_dish.html',{'Dishes' : Dishes})

@login_required
def SelectPriceGet(request,table):
    print('-------------In select price ------------------')
    print(request.POST)
    id = request.POST['id']
    obj = Dish.objects.get(dish_name=id)
    print(obj, obj.price)
    return HttpResponse(json.dumps(obj.price), content_type='application/json')

@login_required
def Delete_dish(request,dish_id):
    obj1 = Dish.objects.get(dish_id=dish_id)
    obj2 = DefaultDish.objects.get(dish_name_Def = obj1.def_dish_id)
    # from OrderAndDish.models import DefaultDish
    dishes = Dish.objects.all()
    if obj1.delete():
        obj2.active = 1;
        obj2.save()
        dishes = Dish.objects.all()
        return render(request, 'CustomerAndDish/index_dishes.html', {'dishes': dishes},messages.success(request, 'Order was successfully deleted.', 'alert-success'))
    else:
        return render(request, 'CustomerAndDish/index_dishes.html', {'dishes': dishes},messages.success(request, 'Cannot delete Order.', 'alert-danger'))

def Edit_dish(request,dish_id):
    obj1 = Dish.objects.get(dish_id=dish_id)
    Dishes = DefaultDish.objects.filter(active=1)
    if request.POST:
        obj1.category = request.POST['new_Category']
        obj1.subcategory = request.POST['new_SubCategory']
        obj1.price = request.POST['new_DishPrice']
        Dishes = Dish.objects.all()
        if obj1.save():
            return render(request, 'CustomerAndDish/index_dishes.html', {'dishes': Dishes},
                          messages.success(request, 'Cannot edit Dish ['+obj1.dish_name+']', 'alert-danger'))
        else:
            return render(request, 'CustomerAndDish/index_dishes.html', {'dishes': Dishes},
                          messages.success(request, 'Dish was successfully edited ['+obj1.dish_name+'] !', 'alert-success'))

    return render(request, 'CustomerAndDish/edit_dish.html' ,{'dishObj':obj1 ,'Dishes':Dishes} )

@login_required
def Table_Layout(request):
    print('In table Layout')
    # room_tables = {}
    all_roomTables = RoomTable.objects.all()
    print(all_roomTables)
    if request.POST:
        room_name = request.POST['room_name']
        table_nos = request.POST['table_nos']
        room_table_obj = RoomTable(room_name = room_name,room_tables=table_nos)
        room_table_obj.save()
        # print(room_name,table_nos)
        all_roomTables = RoomTable.objects.all()
        return render(request, 'CustomerAndDish/layout_table.html',{'all_roomTables':all_roomTables })
    return render(request,'CustomerAndDish/layout_table.html',{'all_roomTables':all_roomTables})

@login_required
def TableInfo_DataInput(request):
    all_roomTables = RoomTable.objects.all()
    print('----------In layout submit----------')
    for i in all_roomTables:
        table_room = i.room_name
        total_tables = i.room_tables
        for j in range(1,int(total_tables)+1):
            table_n = table_room.replace(' ', "") + '.' + str(j)
            TableInfo.objects.create(
                table_room=table_room,
                table_no=j,
                table_n=table_n
            )
    return HttpResponse('submited')

@login_required
def order_screen_redirect(request, table):
    return redirect('newOrder', table)

