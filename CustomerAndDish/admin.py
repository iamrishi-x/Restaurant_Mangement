from django.contrib import admin

# Register your models here.
from .models import Dish,DefaultDish,Customer,Customer_Dish,RoomTable,TableInfo
admin.site.register(Dish)
admin.site.register(DefaultDish)
admin.site.register(Customer)
admin.site.register(Customer_Dish)
admin.site.register(RoomTable)
admin.site.register(TableInfo)