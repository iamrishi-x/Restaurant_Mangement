from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
    #For Tables
    path('', views.Table_View,name="tableView"),
    path('table_layout/', views.Table_Layout,name="tableLayout"),
    path('TableInfo_DataInput/', views.TableInfo_DataInput,name="TableInfo_DataInput"),

    #For Orders
    path('all_order/', views.All_Order,name="allOrder"),
    path('new_order/<str:table>', views.New_Order,name="newOrder"),
    path('new_order/<str:table>/AddDish', views.AddDish,name='AddDish'),
    path('order_redirect/<str:table>', views.order_screen_redirect, name='order_redirect'),
    # path('order_info/<str:pk>', views.order_screen, name='order_info_url'),
    url(r'^print/(?P<cust_id>\d+)/$', views.Print_Order, name='printOrder'),
    url(r'^edit/(?P<cust_id>\d+)/$', views.Edit_Order, name='editOrder'),
    url(r'^delete/(?P<cust_id>\d+)/$', views.Delete_Order, name='deleteOrder'),

    #For Dishes
    path('all_dish/', views.All_Dish,name="allDish"),
    path('new_dish/', views.New_Dish,name="newDish"),
    path('new_order/<str:table>/SelectPriceGet', views.SelectPriceGet,name='selectPriceGet'), #This is Ajax Function For Dish Price Populate
    path('delete_dish/<str:dish_id>/', views.Delete_dish, name='deleteDish'),
    path('edit_dish/<str:dish_id>/', views.Edit_dish, name='editDish'),
]

