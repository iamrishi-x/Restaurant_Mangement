from django.db import models
from datetime import datetime

#user - admin
#pass - admin#123

class DefaultDish(models.Model):
    dish_name_Def = models.CharField(db_column="dish", max_length=100)
    category = models.CharField(db_column="category",max_length=100)
    subcategory = models.CharField(db_column="subcategory",max_length=100)
    active = models.IntegerField(default='1')

    def __str__(self):
        return str(f'{self.dish_name_Def}')

class RoomTable(models.Model):
    room_name = models.CharField(max_length=255, blank=False, null=False) #like AC ,Party , Ordinary
    room_tables = models.SmallIntegerField(blank=True, null=True, default=0)
    room_n = models.CharField(max_length=255, editable=False, null=False, default='a') #for concatination

    def __str__(self):
        return self.room_name

    def save(self, *args, **kwargs):
        self.room_n = str(self.room_name).replace(' ', "")
        super(RoomTable, self).save(*args, **kwargs)

class Dish(models.Model):
    dish_id = models.AutoField(primary_key=True)
    def_dish_id = models.ForeignKey(DefaultDish,on_delete=models.CASCADE,default="")
    dish_name = models.CharField(max_length=50,default=def_dish_id)
    category = models.CharField(max_length=50,default='--')
    subcategory = models.CharField(max_length=50,default='--')
    active = models.CharField(max_length=50,default=1)
    date_created = models.DateField(default=datetime.now, blank=True)
    price = models.IntegerField()

    def __str__(self):
        return str(f'{self.def_dish_id}')

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    table = models.CharField(max_length=255, blank=True, verbose_name='Table No.', null=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20,blank=True)
    address = models.TextField(blank=True)
    date = models.DateField(blank=True)
    time_in = models.TimeField(blank=True)
    payment_option = models.CharField(max_length=50) # Post pay / Pre Pay
    order_type = models.CharField(max_length=50)  #Dine In / Take Away
    order_status = models.CharField(max_length=50)
    order_total = models.IntegerField(blank=True) #Total bill
    no_of_people = models.IntegerField(blank=True)

    def __str__(self):
        return str(f'{self.name}')

class Customer_Dish(models.Model): #Invoice
    class Meta:
        unique_together = (('cust_id', 'dish_id'),)
    cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    dish_id =  models.ForeignKey(Dish,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    dish_price = models.IntegerField()
    dish_row_total = models.IntegerField() #quantity * dishPrice

    def __str__(self):
        return str(f'{self.cust_id}-{self.dish_id}')

class TableInfo(models.Model):
    cust_id = models.ForeignKey(Customer, on_delete=models.SET_NULL,default='',blank=True, null=True)
    table_room = models.CharField(max_length=200, blank=False, null=False)
    table_no = models.SmallIntegerField(null=False)
    table_n = models.CharField(max_length=200, blank=True, null=True)
    in_time = models.DateTimeField(auto_now=True)
    is_close = models.BooleanField(default=0)

    def __str__(self):
        return str(f'{self.table_room}.{self.table_no}')
