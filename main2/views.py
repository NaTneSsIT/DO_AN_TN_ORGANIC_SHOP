from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max, Avg, Count
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core import serializers
from .models import Category, Brand, Product, Size, ProductAttribute, CartOrder, CartOrderItems, UserAddressBook, \
    ProductReview, Wishlist
from main2.forms import SignupForm, ReviewAdd, ProfileForm, AddressBookForm
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.forms.models import model_to_dict

# Create your views here.
def home(request):
    data = Product.objects.filter(is_special=True).order_by('-id')
    cate = Category.objects.all()
    brand = Brand.objects.all()
    return render(request, 'index.html', {'data': data, 'cate': cate, 'brand': brand})


def categories_list(request):
    data = Category.objects.all()
    return render(request, 'categories.html', {"data": data})


def brands_list(request):
    data = Brand.objects.all()
    return render(request, 'brands.html', {"data": data})


def products_list(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:6]
    min_price = ProductAttribute.objects.aggregate(Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))
    return render(request, 'products.html',
                  {"data": data,
                   'total_data': total_data,
                   "min_price": min_price,
                   "max_price": max_price})


def category_product_list(request, cate_id):
    cate = Category.objects.get(id=cate_id)
    data = Product.objects.filter(category=cate)
    return render(request, 'category_product_list.html', {"data": data, "cate": cate})


def brand_product_list(request, brand_id):
    bra = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=bra)
    return render(request, 'brand_product_list.html', {"data": data, "bra": bra})


def product_detail(request, slug, id):
    product = Product.objects.get(id=id)
    attribute = ProductAttribute.objects.filter(product=product)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    sizes = ProductAttribute.objects.filter(product=product).values('size_id', 'size__size_name', 'price').distinct()
    reviewForm = ReviewAdd()

    # Check
    canAdd = True
    reviewCheck = ProductReview.objects.filter(user=request.user, product=product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False
    # End

    # Fetch reviews
    reviews = ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'product_detail.html',
                  {'data': product, 'attribute': attribute, 'related': related_products, 'sizes': sizes,
                   'reviewForm': reviewForm,
                   'canAdd': canAdd, 'reviews': reviews, 'avg_reviews': avg_reviews})


def search(request):
    q = request.GET['q']
    data = Product.objects.filter(product_name__icontains=q).order_by('-id')
    return render(request, 'search.html', {'data': data})


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t = render_to_string('ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})


def load_more_data(request):
    offset = int(request.GET['offset']) + 6
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset + limit]
    t = render_to_string('ajax/product-list.html', {'data': data})
    return JsonResponse({'data': t})


def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    attribute = ProductAttribute.objects.get(product_id=request.GET['id'], price=request.GET['price'])
    cart_p[str(request.GET['id']) + str(attribute.size.size_name)] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'attribute': attribute.size.size_name,
        'qty_max': attribute.qty
    }
    if 'cartdata' in request.session:
        if str(str(request.GET['id']) + str(attribute.size.size_name)) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id']) + str(attribute.size.size_name)]['qty'] = int(
                cart_p[str(request.GET['id']) + str(attribute.size.size_name)]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


def cart_list(request):
    total_amt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])
        return render(request, 'cart.html',
                      {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                       'total_amt': total_amt})
    else:
        return render(request, 'cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt})


def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart-list.html',
                         {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                          'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart-list.html',
                         {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                          'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('home')
    form = SignupForm
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def checkout(request):
    total_amt = 0
    totalAmt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty']) * float(item['price'])
        # Order
        order = CartOrder.objects.create(
            user=request.user,
            total_amt=totalAmt
        )
        # End
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])
            # OrderItems
            CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-' + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )
        # End
        # Process Payment
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_amt,
            'item_name': 'OrderNo-1' + str(order.id),
            'invoice': 'INV-1' + str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        address = UserAddressBook.objects.filter(user=request.user, status=True).first()
        request.session['order_id'] = order.id
        request.session['order_amount'] = order.total_amt
        return render(request, 'checkout.html',
                      {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                       'total_amt': total_amt, 'form': form, 'address': address})


@csrf_exempt
def payment_done(request):
    order_id = request.session['order_id']
    order_am = request.session['order_amount']
    user_add = UserAddressBook.objects.filter(user=request.user, status=True)
    t = render_to_string('email.html',
                         {'user_add': user_add[0].address, 'user_phone': user_add[0].mobile, 'order_id': order_id,
                          'order_am': order_am, 'user': request.user, 'cart_data': request.session['cartdata']})
    if 'cartdata' in request.session:
        request.session['cartdata'] = {}
    email_order = request.user.email
    order_item = CartOrderItems.objects.filter(order_id=order_id)
    total_qty = 0
    for item in order_item:
        attr = ProductAttribute.objects.filter(product__product_name=item.item, price=item.price)
        total_qty += item.qty
        for at in attr:
            at.qty -= item.qty
            at.save()
    attributes = ProductAttribute.objects.all()
    remaining = 0
    for attribute in attributes:
        remaining += attribute.qty
    order = CartOrder.objects.filter(id=order_id).update(paid_status=True, order_status='Ready to ship', qty=total_qty, qty_remaining = remaining)
    email = EmailMessage('Thank for shopping in ORGANIC SHOP', t, settings.EMAIL_HOST_USER, [email_order])
    email.content_subtype = 'html'
    email.fail_silently = False
    email.send()
    returnData = request.POST
    user = request.user

    return render(request, 'payment-success.html', {'data': returnData, 'user': user, 'order': order})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment-fail.html')


def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})


import calendar


def my_dashboard(request):
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(
        count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request, 'user/dashboard.html', {'monthNumber': monthNumber, 'totalOrders': totalOrders})


# My Orders
def my_orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html', {'orders': orders})


# Order Detail
def my_order_items(request, id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html', {'orderitems': orderitems})


def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/wishlist.html', {'wlist': wlist})


# My Reviews
def my_reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/reviews.html', {'reviews': reviews})


# My AddressBook
def my_addressbook(request):
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/addressbook.html', {'addbook': addbook})


# Save addressbook
def save_address(request):
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm
    return render(request, 'user/add-address.html', {'form': form, 'msg': msg})


# Activate address
def activate_address(request):
    a_id = str(request.GET['id'])
    UserAddressBook.objects.update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool': True})


# Edit Profile
def edit_profile(request):
    msg = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Data has been saved'
    form = ProfileForm(instance=request.user)
    return render(request, 'user/edit-profile.html', {'form': form, 'msg': msg})


# Update addressbook
def update_address(request, id):
    address = UserAddressBook.objects.get(pk=id)
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm(instance=address)
    return render(request, 'user/update-address.html', {'form': form, 'msg': msg})


def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


def cancel_order(request):
    order_id = request.GET['order_id']
    od = CartOrder.objects.filter(id=order_id)
    if od[0].order_status != "Waiting Payment":
        order_item = CartOrderItems.objects.filter(order_id=order_id)
        for item in order_item:
            attr = ProductAttribute.objects.filter(product__product_name=item.item, price=item.price)
            for at in attr:
                at.qty += item.qty
                at.save()
    order = CartOrder.objects.filter(id=order_id).update(order_status='Cancel')
    return JsonResponse({"order":order}, status=200)

def send_mail1(request):
    return render(request, 'email.html')
def statical(request):
    user = request.user
    return render(request, 'statical.html', {'user': user})
def statical1(request):
    start_date = '2023-09-08'
    end_date = '2023-09-09'
    if request.GET.get('start_date', {}):
        start_date = request.GET['start_date']
    if request.GET.get('end_date', {}):
        end_date = request.GET['end_date']
    orders = CartOrder.objects.filter(order_dt__range=[start_date, end_date])
    list_month = list()
    total = []
    total_qty = []
    for order in orders:
        list_month.append(order.order_dt.month)
    list_month = list(set(list_month))
    for month in list_month:
        total_by_month = 0
        qty_by_month = 0
        for order in orders:
            if order.order_dt.month == month and order.order_status != 'cancel':
                total_by_month += order.total_amt
                qty_by_month += order.qty
        total.append(total_by_month)
        total_qty.append(qty_by_month)
    list_remaining = []
    for index, month in enumerate(list_month):
        list_remaining_month = []
        for order in orders:
            if order.order_dt.month == month and order.order_status != 'cancel':
                list_remaining_month.append(order.qty_remaining)
        # list_month[index] = str(list_month[index]) + '(' + str(list_remaining_month[-1]) + ')'
        list_remaining.append(list_remaining_month[-1])
    return render(request, 'order_report.html', {"month": list_month, "total": total, "qty": total_qty, "qty_re": list_remaining})