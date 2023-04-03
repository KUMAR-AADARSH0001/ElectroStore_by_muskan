from django.urls import path
from myapp import views

app_name='myapp'
 
urlpatterns = [
    path('usregister/',views.usregister,name='usregister'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('uservalid/',views.uservalid,name='uservalid'),
    path('about/',views.about,name='about'),
    path('showproducts/',views.showproducts,name='showproducts'),
    path('singleproduct/',views.singleproduct,name='singleproduct'),
    path('mail/',views.usermail,name='mail'),
    path('base/',views.base,name='base'),
    path('cart/',views.addcart,name='cart'),
    path('removecart/',views.removeCart,name='removecart'),
    path('grandTotal/',views.grandTotal,name='grandTotal'),
    path('sendMail/',views.sendMail,name='sendMail'),
    path('success_payment/',views.success_payment, name='success_payment'),
    path('get_order/',views.get_order, name='get_order'),
    path('orders/',views.orders, name='orders'),
    path('pending_orders/',views.pending_orders, name='pending_orders'),
    path('profile/',views.profile, name='profile'),
    path('change_profile/',views.change_profile, name='change_profile'),
    path('singleorder/',views.singleorder, name='singleorder'),
    path('change_password/',views.change_password, name='change_password'),
    path('order_detail/',views.order_detail, name='order_detail'),
]