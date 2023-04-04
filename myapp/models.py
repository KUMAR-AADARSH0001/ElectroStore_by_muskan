from django.db import models
from django.contrib.auth.models import User


class customer(models.Model):
    Gender = (("MALE", "MALE"),
              ("FEMALE", "FEMALE"),
              ("NOT DEFINE", "NOT DEFINE"),)
    subtitle = models.CharField(choices=Gender, max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.FileField(upload_to='profiles/%Y/%m/%d', blank=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class category(models.Model):
    category_name = models.CharField(max_length=250)
    sub_cat = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class brands(models.Model):
    brand_name = models.CharField(max_length=250)
    brand_logo = models.ImageField(upload_to='brands/%Y/%m/%d', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name


class product(models.Model):
    product_name = models.CharField(max_length=300)
    product_category = models.ForeignKey(
        category, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    brand = models.ForeignKey(brands, on_delete=models.CASCADE)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    type = models.IntegerField(null=True, blank=True, default=0)

    create_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class order(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    contact_name = models.CharField(max_length=250)
    contact_number = models.CharField(max_length=250)
    contact_email = models.CharField(max_length=250)
    delivery_address = models.CharField(max_length=250)
    txn_id = models.CharField(max_length=250, blank=True)
    payment_mode = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, blank=True)
    cart_id = models.CharField(max_length=500, null=True)
    received_on = models.DateTimeField(auto_now_add=True)
    changed_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)


class mail(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField()
    message = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
