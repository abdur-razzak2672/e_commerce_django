from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE , null=True , blank=True)
    name = models.CharField(max_length=200, null =True)
    email = models.CharField(max_length=200, null =True)
    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200, null =True)
    price = models.FloatField()
    Digital = models.BooleanField(default=False, null=True , blank=True)
    image = models.ImageField(blank = True, null =True)

    def __str__(self):
        return str(self.name)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL , null=True , blank=True)
    data_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True , blank=True)
    transaction_id = models.CharField(max_length=200, null =True)

    @property
    def shipping(self):
        shiping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
             if i.product.Digital == False:
                shipping = True  
        return shipping

        

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()

        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()

        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL , null=True , blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL , null=True , blank=True)
    quantity = models.IntegerField(default=0, null=True , blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price* self.quantity
        return total

        


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL , null=True , blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL , null=True , blank=True)
    address = models.CharField(max_length=200, null =True)
    city = models.CharField(max_length=200, null =True)
    state = models.CharField(max_length=200, null =True)
    zipcode = models.CharField(max_length=200, null =True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.address)


