from django.contrib.auth import authenticate, get_user_model, login, logout
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from myapp.forms import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from myapp.models import customer, brands, category, product, mail, cart, order
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib import messages
import json
import math
from django.db.models import Q
import random
from django.core.mail import EmailMessage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password


@csrf_exempt
def payment_done(request):
    return HttpResponse('Payment Successful')


def logout_view(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def payment_canceled(request):
    return HttpResponse('Payment Canceled')


# Brands carousel
all_brands = brands.objects.all().order_by('-id')
# categories
cat = category.objects.filter(sub_cat=None)

# latest products
lp = product.objects.all().order_by('-id')[:4]

# total offer percentage
all_products = product.objects.all()

# get user


def getloginuser(id):
    ruser = User.objects.get(username=id)
    cust = customer.objects.get(user=ruser)
    details = {
        'id': ruser.id,
        'first_name': ruser.first_name,
        'username': ruser.username,
        'subtitle': cust.subtitle,
        # 'address': cust.address,
        'profile_pic': cust.profile_pic,
        'custid': cust.id,
        'registered_on': cust.registered_on,
    }
    return details


def all_cats():
    # All Categories with sub categories
    main = []
    for i in cat:
        ab = []
        ab.append(i.category_name)
        ab += list(category.objects.filter(sub_cat=i).values())
        main.append(ab)
    return main


def base(request):
    return render(request, 'base.html', {'cattt': cat})


def index(request):
    form = UserLoginForm()
    form1 = profileform()

    total = 0
    sale = 0
    each = []
    for i in all_products:
        discount = (math.ceil(100-(i.sale_price/i.price*100)))
        ep = {'id': i.id, 'd': discount}
        each.append(ep)
        total += i.price
        sale += i.sale_price
    offer = 0
    pid = 0
    for m in each:
        if m['d'] > offer:
            offer = m['d']
            pid = m['id']
    getproduct = product.objects.get(id=pid)
    total_offer = math.ceil(100-(sale/total*100))
    if request.method == 'GET':
        if 'cat' in request.GET:
            c = request.GET['cat']
            catobject = category.objects.get(category_name=c)
            dt = category.objects.filter(sub_cat=catobject).values()
            ab = []
            for i in dt:
                sub_cat = category.objects.get(id=i['id'])
                ab += list(product.objects.filter(product_category=sub_cat).values())
            products = product.objects.filter(
                product_category=catobject).values()
            allproducts = list(products)
            final = ab+allproducts
            return JsonResponse(final, safe=False)

        if 'prid' in request.GET:
            id = request.GET['prid']
            singlep = product.objects.get(id=id)
            abcd = {"id": singlep.id, "name": singlep.product_name, "price": str(singlep.price), "sale_price": str(
                singlep.sale_price), "photo": str(singlep.photo), "brand": str(singlep.brand), "description": singlep.description}
            dump = json.dumps(abcd)
            return HttpResponse(dump, content_type='application/json')

    return render(request, 'index.html', {'form': form, 'form1': form1, 'brands': all_brands, 'cat': cat, 'allcat': all_cats(), 'to': total_offer, 'eoff': offer, 'epnm': getproduct.product_name, 'eimg': getproduct.photo, 'lp': lp})


def usregister(request):
    if "username" in request.COOKIES and "id" in request.COOKIES:
        usn = request.COOKIES['username']
        id = request.COOKIES['id']
        user = User.objects.get(pk=id)
        login(request, user)
        return HttpResponseRedirect('/myapp/dashboard')
    elif request.method == 'POST':
        if 'signup' in request.POST:
            form = userform(data=request.POST)
            form1 = profileform(data=request.POST)
            if form.is_valid() and form1.is_valid():
                user = form.save()
                user.set_password(user.password)
                user.save()

                profile = form1.save(commit=False)
                profile.user = user
                profile.save()

                if "profile_pic" in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']
                    print("Success")
                profile.save()
                response = "register Successfully"

                return render(request, 'index.html', {'response': response})


def uslogin(request):
    form = UserLoginForm()
    form1 = profileform()
    if "username" in request.COOKIES and "id" in request.COOKIES:
        usn = request.COOKIES['username']
        id = request.COOKIES['id']
        user = User.objects.get(pk=id)
        login(request, user)
        return HttpResponseRedirect('/myapp/dashboard')
    if request.method == 'POST':
        if 'signin' in request.POST:
            em = request.POST['Email']
            pas = request.POST['Password']
            user = authenticate(username=em, password=pas)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session['id'] = em
                    request.session['type'] = 'customer'
                    response = HttpResponseRedirect('/myapp/profile')
                    if "remember" in request.POST:
                        response.set_cookie('username', em)
                        response.set_cookie('id', user.id)
                        response.set_cookie(
                            'last_connection', datetime.datetime.now())
                        print("COOKIES CREATED")
                        return response
                    else:
                        return response
            else:
                response = 'Sorry, You Are Not Registered User'
                return render(request, 'index.html', {'form': form, 'form1': form1, 'response': response})


@login_required
def dashboard(request):
    us = getloginuser(request.session['id'])
    return render(request, 'dashboard.html', {'pp': us, 'cat': cat})


@login_required
def uslogout(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('username')
    response.delete_cookie('id')
    return response


def authemail(request):
    return HttpResponseRedirect('/myapp/dashboard/')


def uservalid(request):
    if request.method == 'GET':
        if 'username' in request.GET:
            un = request.GET['username']
            check = User.objects.filter(username=un)
            if (len(check) > 0):
                return HttpResponse('A user with this name already exists')

            else:
                return HttpResponse('Success')
# About page


def about(request):
    return render(request, 'about.html', {'cat': cat, 'allcat': all_cats()})

# products page


def showproducts(request):
    products = product.objects.all().order_by('-id')
    main = []
    for i in cat:
        ab = []
        ab.append(i.category_name)
        ab.append(i.id)
        ab += list(category.objects.filter(sub_cat=i).values())
        main.append(ab)

    # Filter by category
    if 'searchcat' in request.GET or 'scat' in request.GET:
        filcat = request.GET['searchcat']
        scat = request.GET['scat']

        searched_cat = category.objects.get(category_name=scat)
        products = product.objects.filter(
            product_category=searched_cat).order_by('-id')

        # Related Products
        searched_cat2 = category.objects.get(category_name=filcat)
        dt = category.objects.filter(sub_cat=searched_cat2).values()
        ab = []
        for i in dt:
            sub_cat = category.objects.get(id=i['id'])
            ab += list(product.objects.filter(product_category=sub_cat).values())
        rlproducts = product.objects.filter(
            product_category=searched_cat2).values()
        allproducts = list(rlproducts)
        final = ab+allproducts
        print(final)

        # products2= product.objects.filter(product_category=searched_cat2).order_by('-id')
        return render(request, 'showproducts.html', {'allcat': main, 'p': products, 'rp': final, 'total': len(products), 'cat': cat})

    if 'Search' in request.POST:
        userSearch = request.POST['searchproduct']
        srchResult = product.objects.filter(Q(product_name__icontains=userSearch) | Q(product_category__category_name__icontains=userSearch) | Q(
            description__icontains=userSearch) | Q(brand__brand_name__icontains=userSearch))
        total = len(srchResult)

        return render(request, 'showproducts.html', {'allcat': main, 'p': srchResult, 'cat': cat, 'total': total})

    if 'deal' in request.GET:
        today = str(datetime.date.today()).split('-')[2]
        todayproducts = product.objects.filter(create_date__day=today)
        total = len(todayproducts)
        return render(request, 'showproducts.html', {'allcat': main, 'p': todayproducts, 'cat': cat, 'total': total})

    if 'min' in request.GET:
        min = request.GET['min']
        max = request.GET['max']
        rangep = product.objects.filter(
            sale_price__gte=min, sale_price__lte=max)
        total = len(rangep)
        return render(request, 'showproducts.html', {'allcat': main, 'p': rangep, 'cat': cat, 'total': total})

    elif 'above' in request.GET:
        above = request.GET['above']
        rangep = product.objects.filter(
            sale_price__gte=above, sale_price=above)
        total = len(rangep)
        return render(request, 'showproducts.html', {'allcat': main, 'p': rangep, 'cat': cat, 'total': total})

    return render(request, 'showproducts.html', {'allcat': main, 'p': products, 'cat': cat})


def singleproduct(request):
    productid = request.GET['singlep']
    product_detail = product.objects.get(id=productid)

    # Related Products
    searched_cat2 = category.objects.get(
        category_name=product_detail.product_category)
    ab = product.objects.filter(product_category=searched_cat2)
    # dt = category.objects.filter(sub_cat=searched_cat2).values()
    # ab = []
    # for i in dt:
    #     sub_cat = category.objects.get(id=i['id'])
    #     ab += list(product.objects.filter(product_category=sub_cat).values())
    # print('ZXCVB',ab)

    arr = product_detail.description.split('@')
    details = {
        'id': product_detail.id,
        'pname': product_detail.product_name,
        'price': product_detail.price,
        'sprice': product_detail.sale_price,
        'cat': product_detail.product_category,
        'photo': product_detail.photo,
        'brand': product_detail.brand,
        'description': arr,
        'create_date': product_detail.create_date,
        'rp': ab,
        'cat': cat,
        'allcat': all_cats()
    }
    return render(request, 'singleproduct.html', details)


def usermail(request):
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        phone = request.POST['Telephone']
        msz = request.POST['message']

        message = mail(name=name, email=email, phone=phone, message=msz)
        message.save()
        return render(request, 'mail.html', {'cat': cat, 'status': True, 'name': name})

    return render(request, 'mail.html', {'cat': cat, 'allcat': all_cats()})


def addcart(request):
    if 'id' in request.session.keys():
        cust = User.objects.get(username=request.session['id'])
        viewCart = cart.objects.filter(user_id=cust, type=0)
        total_cart = []
        if request.method == 'POST':
            item = request.POST['item_id']
            price = request.POST['amount']
            qty = request.POST['add']

            check = cart.objects.filter(type=0)
            product_object = product.objects.get(id=item)
            exist = False
            for x in check:
                if x.product_id == product_object and x.user_id == cust:
                    exist = True
            if exist is True:
                messages.warning(request, 'Item Already in Your Cart')
            else:
                saveCart = cart(
                    user_id=cust, product_id=product_object, quantity=qty)
                saveCart.save()
                messages.success(request, 'Item Added to Your Cart')

        if 'q' in request.GET:
            newQ = request.GET['q']
            cartId = request.GET['id']
            getCart = cart.objects.get(id=cartId)
            getCart.quantity = newQ
            getCart.save()
            details = {
                'quantity': getCart.quantity,
                'sale_price': getCart.product_id.sale_price,
                'price': getCart.product_id.price,
                'cart_size': len(viewCart),
            }
            return JsonResponse(details)
        cid = ''
        for x in viewCart:
            cid += str(x.id)+'/'
            user_cart = {}
            user_cart['id'] = x.id
            user_cart['product_name'] = x.product_id.product_name
            user_cart['photo'] = x.product_id.photo
            user_cart['product_cat'] = x.product_id.product_category
            user_cart['quantity'] = x.quantity
            user_cart['price'] = x.product_id.sale_price
            user_cart['market'] = x.product_id.price
            user_cart['brand'] = x.product_id.brand
            user_cart['offer'] = math.ceil(
                100-(x.product_id.sale_price/x.product_id.price)*100)
            total_cart.append(user_cart)

        return render(request, 'cart.html', {'cart': total_cart, 'cart_size': len(total_cart), 'cids': cid, 'allcat': all_cats(), 'cat': cat, 'pp': getloginuser(request.session['id'])})
    else:
        messages.info(request, 'You need to login first!!!')
        return render(request, 'cart.html', {'allcat': all_cats(), })


@login_required
def removeCart(request):
    if 'id' in request.session.keys():

        if request.method == 'GET':
            id = request.GET['removeid']
            deleteObj = cart.objects.get(id=id)
            deleteObj.type = 1
            deleteObj.save()

            # User Cart
            cust = User.objects.get(username=request.session['id'])
            viewCart = cart.objects.filter(user_id=cust)
            cart_size = len(viewCart)

            data = {
                'msz': 'Item Removed Successfully!!!',
                'cart_size': cart_size,
            }
            return JsonResponse(data)
    else:
        messages.info(request, 'You need to login first!!!')
        return render(request, 'cart.html', {'allcat': all_cats()})


@login_required
def grandTotal(request):
    if 'id' in request.session.keys():
        cust = User.objects.get(username=request.session['id'])
        cc = customer.objects.get(user=cust)
        viewCart = cart.objects.filter(user_id=cust, type=0)
        grand_total = 0
        quantity = 0
        for i in viewCart:
            grand_total = grand_total+(i.product_id.sale_price*i.quantity)
            quantity = quantity+i.quantity

        data = {
            'grand_total': grand_total,
            'quantity': quantity,
            'email': cust.username,
            'name': cust.first_name,
            'address': cc.address
        }

        return JsonResponse(data)


def sendMail(request):
    otp = random.randint(100000, 999999)
    try:
        name = 'Customer'
        print(otp)
        subject = 'Account Activation'
        if 'name' in request.GET:
            name = request.GET['name']
        message = 'Dear {}, \n {} is your One Time Password for registration \n Thanks for being a part of our organization\n Do not share it with anyone'.format(
            name, otp)
        receiver = str(request.GET['email'])
        email = EmailMessage(subject, message, to=[receiver,])
        email.send()
        response = ['An OTP Sent to your Email Address @', otp]
        return HttpResponse(response)
    except:
        response = ['OOPs!! Error Occured @', otp]
        return HttpResponse(response)


@login_required
def get_order(request):
    if 'id' in request.session.keys():
        us = User.objects.get(username=request.session['id'])
        cust = customer.objects.get(user=us)
        if request.method == 'GET':
            dnm = request.GET['dname']
            dem = request.GET['demail']
            dmn = request.GET['dnumber']
            addr = request.GET['daddress']
            amt = request.GET['grandtotal']
            items = request.GET['items']

            order_obj = order(customer=cust, amount=amt, contact_name=dnm,
                              contact_number=dmn, contact_email=dem, delivery_address=addr, cart_id=items)
            order_obj.save()
            oid = order_obj.id

            return HttpResponse(oid)


@login_required
def success_payment(request):
    if 'ORDERID' in request.GET:
        order_id = request.GET['ORDERID']
        txn_id = request.GET['TXNID']
        pay_mode = request.GET['PAYMENTMODE']
        bank_name = request.GET['BANKNAME']

        sid = order_id.split('o')[0]
        order_obj = order.objects.get(id=int(sid))
        order_obj.txn_id = txn_id
        order_obj.payment_mode = pay_mode
        order_obj.bank_name = bank_name
        order_obj.status = True
        order_obj.save()

        try:
            all_items = order_obj.cart_id
            if all_items != '' or all_items != None:
                ls = all_items.split('/')
                for cid in ls[:-1]:
                    citem = cart.objects.get(id=cid)
                    citem.type = 1
                    citem.save()
        except:
            return render(request, 'process.html', {'status': 'Something went wrong!!!', 'allcat': all_cats(), 'cat': cat})

        return render(request, 'process.html', {'txn_id': txn_id, 'allcat': all_cats(), 'cat': cat})


@login_required
def orders(request):
    us = User.objects.get(username=request.session['id'])
    cust = customer.objects.get(user=us)
    ords = order.objects.filter(customer=cust, status=True)
    details = getloginuser(request.session['id'])
    return render(request, 'orderes.html', {'all_orders': ords, 'allcat': all_cats(), 'cat': cat, 'pp': details})


@login_required
def pending_orders(request):
    us = User.objects.get(username=request.session['id'])
    cust = customer.objects.get(user=us)
    ords = order.objects.filter(customer=cust, status='')
    details = getloginuser(request.session['id'])
    return render(request, 'pending.html', {'pending_orders': ords, 'allcat': all_cats(), 'cat': cat, 'pp': details})


@login_required
def profile(request):
    details = getloginuser(request.session['id'])
    return render(request, 'profile.html', {'allcat': all_cats(), 'cat': cat, 'pp': details})


@login_required
def change_profile(request):
    details = getloginuser(request.session['id'])
    if request.method == 'POST':
        first_name = request.POST['name']
        subtitle = request.POST['subtitle']
        email = request.POST['email']
        address = request.POST['address']
        userid = request.POST['id']
        custid = request.POST['custid']

        userObj = User.objects.get(id=userid)
        if first_name != '':
            userObj.first_name = first_name
        if email != '':
            userObj.username = email
            request.session['id'] = email
        userObj.save()

        customerObj = customer.objects.get(id=custid)
        if subtitle != '':
            customerObj.subtitle = subtitle
        if address != '':
            customerObj.address = address
        customerObj.save()
        return render(request, 'change_profile.html', {'allcat': all_cats(), 'cat': cat, 'pp': details, 'status': 'Changes saved successfully!!!'})

    return render(request, 'change_profile.html', {'allcat': all_cats(), 'cat': cat, 'pp': details})


def singleorder(request):
    return render(request, 'singleorder.html')


def change_password(request):
    if request.method == 'POST':
        uid = request.POST['id']
        old = request.POST['oldpass']
        npass = request.POST['newpass']

        user = User.objects.get(id=uid)
        if check_password(old, user.password):
            user.set_password(npass)
            user.save()
            messages.success(request, 'Password Changed!!!')

        else:
            messages.error(request, 'Incorrect Current Password')
    return render(request, 'change_password.html', {'allcat': all_cats(), 'cat': cat, 'pp': getloginuser(request.session['id'])})


def order_detail(request):
    if request.method == 'GET':
        id = request.GET['id']
        orders = order.objects.get(id=id)
        items = orders.cart_id
        all_items = items.split('/')
        products = []
        c = 1
        for i in all_items[:-1]:
            p = cart.objects.get(id=i)
            dict = {
                'sr': c,
                'pname': p.product_id.product_name,
                'price': p.product_id.sale_price,
                'photo': p.product_id.photo,
                'quantity': p.quantity,
                'totalprice': p.quantity*p.product_id.sale_price,

            }
            c += 1
            products.append(dict)
    return render(request, 'order_detail.html', {'allcat': all_cats(), 'cat': cat, 'pp': getloginuser(request.session['id']), 'products': products, 'sz': len(products)})
