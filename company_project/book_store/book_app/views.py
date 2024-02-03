from django.shortcuts import render
from.models import UserProfile,Product,Cart
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from.models import UserProfile, Product, Cart
from django.contrib.auth.decorators import user_passes_test
from .models import Order, OrderItem


# def is_admin_or_user(user):
#     return user.is_staff or user.is_authenticated

def is_admin(user):
     return user.is_staff


def base(request):
    return render(request,'base.html')

def base_new(request):
    return render(request,'base_new.html')


def base2_new(request):
    return render(request,'base2_new.html')
    


def account(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        adduser = UserProfile(firstname=firstname, lastname=lastname,  phone=phone, email=email,
                          username=username, password=password)

        auth_user = User(username=username, first_name=firstname, last_name=lastname, email=email)
        auth_user.set_password(password)
        auth_user.save()
        adduser.save()
        return redirect('login') 

    return render(request,'account.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_staff:
                return redirect('base_new')  
            else:
                return redirect('base2_new') 
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')



# def login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth_login(request, user)
#             return redirect('base_new')
#         else:
#             return render(request, 'login.html', {'error_message': 'Invalid username or password'})

#     return render(request, 'login.html')

# @user_passes_test(is_admin_or_user, login_url='login')
# def login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth_login(request, user)
#             return redirect('base_new')
#         else:
#             return render(request, 'login.html', {'error_message': 'Invalid username or password'})

#     return render(request, 'login.html')


@user_passes_test(is_admin, login_url='login')
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES['image']
        if not name or not price or not image:
            return HttpResponse("Please provide all required fields.")

        new_product = Product(name=name, price=price, image=image)
        new_product.save()

        return HttpResponse("Product successfully added.")

    return render(request, 'add_product.html')

# @user_passes_test(is_admin, login_url='login')
# def add_product(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         price = request.POST['price']
#         image = request.FILES['image']
#         if not name or not price or not image:
#             return HttpResponse("Please provide all required fields.")

#         new_product = Product(name=name, price=price, image=image)
#         new_product.save()

#         return HttpResponse("Product successfully added.")

#     return render(request, 'add_product.html')

def product(request):
    Book_items = Product.objects.all()
    return render(request, 'product_page.html', {'bk': Book_items})
 
def product_details(request):
    Book_items = Product.objects.all()
    return render(request,'product_details.html',{'bookdetail':Book_items})

def edit_product(request, product_id):
    try:
        edit_product = get_object_or_404(Product, id=product_id)
    except Product.DoesNotExist:
        return HttpResponse('Product not found')

    if request.method == 'POST':
        edit_product.name = request.POST['name']
        edit_product.price = request.POST['price']
        edit_product.image = request.FILES['image']
        
        edit_product.save()
      
        return HttpResponse('Product edited successfully')
    return render(request, 'edit.html', {'edit_product': edit_product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_details')
    
    return HttpResponse('Invalid request for product deletion')


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    return redirect('cart')

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.calculate_total() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def update_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item = Cart.objects.get(user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart')

def remove_from_cart(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)
        Cart.objects.filter(user=request.user, product=product).delete()

    return redirect('cart')

def user_logout(request):
    logout(request)
    return redirect('base')  

# def checkout(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     total_price = sum(item.calculate_total() for item in cart_items)
#     return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.calculate_total() for item in cart_items)

    if request.method == 'POST':
        # Extract form data and create an Order instance
        name = request.POST['name']
        phone = request.POST['phone']
        pincode = request.POST['pincode']
        shipping_address = request.POST['shipping_address']

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            name=name,
            phone=phone,
            pincode=pincode,
            total_price=total_price
        )

        # Create OrderItem instances for each item in the cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear the user's cart after placing the order
        Cart.objects.filter(user=request.user).delete()

        return render(request, 'order_confirmation.html', {'order': order})

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def order_confirmation(request):
    return render(request, 'order_confirmation.html')