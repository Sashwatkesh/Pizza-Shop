from urllib import response
from django.shortcuts import render,redirect
from .models import*
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#instamojo Payment Gateway
from instamojo_wrapper import Instamojo
from django.conf import settings
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN , endpoint='https://test.instamojo.com/api/1.1/')



# Create your views here.
def home(request):
    pizzas = Pizza.objects.all()
    data = {
        'pizzas':pizzas,
    }
    return render(request,'home.html',data)

@login_required(login_url='/login/')
def Add_Cart(request,pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uid = pizza_uid)
    cart , _ = Cart.objects.get_or_create(user=user,is_paid = False)


    cart_item = Cart_item.objects.create(
        cart = cart,
        pizza = pizza_obj
    )
    cart_item.save()
    return redirect("/")



from django .contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect

# Create your views here.


def handelsingup(request):
    if request.method=='POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
# Check for input
        if not username.isalnum():
            messages.error(request,"Name should onlu contain letters and numbers ")

        if password!=password2:
            messages.error(request,"Password don't match")
            return redirect("/")
        if len(username) > 10:
            messages.error(request,"To long username")
        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('/')

#create user
    
        myuser = User.objects.create_user(username, email,password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save
        messages.success(request,"Your Account Has Been Created")
        return redirect("/")

    
    return render(request,"singup.html")

def handlogin(request):
    
    if request.method=='POST':
        logusername = request.POST.get('username')
        logpassword = request.POST.get('password')

        user = authenticate(username = logusername,password = logpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Login")
            return redirect("/")  
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect("/")

    return render(request,'login.html')

def handellogout(request):
    logout(request)
    messages.success(request,"Sucessfully Logout")

    return redirect("/")

def success(request):
    payment_request = request.GET.get('payment_request_id')
    cart = Cart.objects.get(instamojo_id = payment_request)
    cart.is_paid = True
    cart.save()
    return render(request,'success.html')



@login_required(login_url='/login/')
def cart(request):
    cart = Cart.objects.get(is_paid = False,user = request.user)
   
    response =api.payment_request_create(
        amount = cart.get_cart_total(),
        purpose='order',
        buyer_name= request.user.username,
        email="shashwat5078844@gmail.com",
        redirect_url='http://127.0.0.1:8000/success/'
    ) 
    print(response)
    cart.instamojo_id = response['payment_request']['id']
    cart.save()
    data = {
        'carts':cart,
        'payment_url':response['payment_request']['longurl']
    
    }
    return render(request,'cart.html',data)
@login_required(login_url='/login/')
def remove_cart_item(request, cart_item_uid):
    try:
        Cart_item.objects.get(uid = cart_item_uid).delete()
        return redirect('/cart/')
    except Exception as e:
        print(e)
        return HttpResponse("403 Page not found")


@login_required(login_url='/login/')
def order(request):
    order = Cart.objects.filter(is_paid = True, user = request.user)

    return render(request,'order.html',{'orders':order})