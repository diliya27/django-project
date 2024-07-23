from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render,redirect

from shop.models import Product
from cart.models import Cart
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from cart.models import Payment
from .models import Order_table


#
from django.views.decorators.csrf import csrf_exempt

import razorpay

# Create your views here.
@login_required
def add_to_cart(request,pk):
    p=Product.objects.get(id=pk)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if(p.stock):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1
            p.save()

    # return HttpResponse('product is added to cart')
    return redirect('cart:cart_view')


@login_required
def cart_view(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total+=i.quantity*i.product.price

    return render(request,'cart.html',{'cart':cart,'total':total})

@login_required
def cart_decrement(request,d):
    p = Product.objects.get(id=d)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if(cart.quantity>1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
            cart.delete()
            p.stock +=1
            p.save()
    except:
        pass

    return redirect('cart:cart_view')


@login_required
def cart_trash(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        q=cart.delete()
        p.stock +=cart.quantity
        p.save()

    except:
        pass
    return redirect('cart:cart_view')

@login_required

def orderform(request):
    if(request.method=='POST'):
        ph=request.POST.get('p')
        a=request.POST.get('a')
        n=request.POST.get('n')
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+(i.quantity*i.product.price)     #Total amount
        total=int(total*100)

        #create Razorpay client using our API credentials
        client=razorpay.Client(auth=('rzp_test_WwAeIbYfM7kzyI','FPK6OKnPtRRvAm0lRNyu6qVt'))

        #create order in Razorpay
        response_payment=client.order.create(dict(amount=total,currency='INR'))
#
#

        print(response_payment)

        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == "created":
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()

            for i in c:
                o=Order_table.objects.create(user=u,product=i.product,address=a,phone=ph,pin=n,no_of_items=i.quantity,order_id=order_id)
                o.save()
        response_payment['name']=u.username

        return render(request,'payment.html',{'payment':response_payment})
#
    return render(request,'place_order.html')

@csrf_exempt
def payment_status(request,u):
    print(request.user.is_authenticated) #false
    if not request.user.is_authenticated:
        user = User.objects.get(username=u)
        login(request,user)
        print(user.is_authenticated) #true

    if(request.method=="POST"):          #Razorpay response after completion of payment
        response=request.POST
        # print(u)
        print(response)
        #to check the authenticity of razorpay signature
        param_dict = {
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_WwAeIbYfM7kzyI','FPK6OKnPtRRvAm0lRNyu6qVt'))
        try:
            status=client.utility.verify_payment_signature(param_dict)# to check the authenticity of razorpay signature
            print(status)

#After sucessful payment

            #retrive a payment record with particular order_id
#         #create payment table enter details
            ord = Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id = response['razorpay_payment_id']#edit payment id response['razorpay_payment_id']
            ord.paid = True# edit paid to true
            ord.save()


            c=Cart.objects.filter(user=user)
            print(user.username)
              #filterthe order_table details for particular user with order_id=response['razorpay_order_id']

            o=Order_table.objects.filter(user=user,order_id=response['razorpay_order_id'])
            print(o)
            for i in o:
                i.payment_status="paid"#edit payment_status="paid
                i.save()
            c.delete() #to delete cart items
            print(status)
            return render(request,'payment_status.html',{'status':True})
        except:
            return render(request,'payment_status.html',{'status':False})

    return render(request,'payment_status.html')

@login_required

def order_view(request):
    u=request.user
    customer=Order_table.objects.filter(user=u,payment_status="paid")


    return render(request,'order_view.html',{'customer':customer,'u':u.username})






