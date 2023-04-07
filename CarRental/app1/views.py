from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import razorpay

# Create your views here.
#client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

def index(request):
    cars = Car.objects.all()
    return render(request, "index.html", {'cars':cars})

Dealer=CarDealer()
def car_dealer_signup(request):
    location = Location.objects.all()
    if request.method == "POST":
        user = CarDealer()
        user.username = request.POST['username']        
        user.email = request.POST['email']
        user.location = request.POST['city']        
        user.phone = request.POST['phone']
        user.password = request.POST['password1']  

        if CarDealer.objects.filter(email=Dealer.email).exists():            
            return redirect('CarDealerSignup') 
        else:
            user.save() 
            return redirect('CarDealerLogin')
    return render(request,"car_dealer_signup.html",{'l':location})

def car_dealer_signout(request):
    if request.session.has_key('email'):
        del request.session['email']
        return redirect('')

def car_dealer_login(request):
    if request.method=="POST":
        try:
            e=request.POST['email'] 
            request.session['email']=e            
            p=request.POST['password']                       
            x=CarDealer.objects.get(email=e)                         
            if x.password==p:
                # messages.success(request, f'you are now logged')                
                return redirect('/all_cars')
            else:
                return redirect('/CarDealerLogin')
        except:
            return redirect('/CarDealerLogin')
    return render(request, "car_dealer_login.html")

def add_car(request):
    if request.session.has_key('email'):
        location = Location.objects.all()
        user = CarDealer.objects.get(email = request.session['email'])
        if request.method == "POST":
            car = Car()
            car.car_dealer = user
            car.name = request.POST['car_name']
            car.location = request.POST['city']
            car.image = request.FILES['image']
            car.capacity = request.POST['capacity']
            car.rent = request.POST['rent']                  
            car.save()                
        return render(request, "add_car.html",{'l':location})

def all_cars(request):
    if request.session.has_key('email'):
        dealer = CarDealer.objects.filter(email=request.session['email']).first()
        cars = Car.objects.filter(car_dealer=dealer)
    return render(request, "all_cars.html", {'cars':cars})

def update_car(request,pk):
    location = Location.objects.all()    
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':            
        car.name = request.POST.get('car_name')
        print(car.name)
        car.location = request.POST.get('city')
        print(car.location)
        car.image = request.POST.get('image')
        print(car.image)
        car.capacity = request.POST.get('capacity')
        print(car.capacity)
        car.rent = request.POST.get('rent')
        print(car.rent)
        car.save()                 
    return render(request,'update_car.html',{'car':car,'l':location})       

def customer_signup(request):
    location = Location.objects.all()
    if request.method == "POST":
        user = Customer()
        user.username = request.POST['username']        
        user.email = request.POST['email']
        user.location = request.POST['city']        
        user.phone = request.POST['phone']
        user.password = request.POST['password1']        
        if Customer.objects.filter(email=user.email).exists():            
            messages.warning(request, 'Email is already Exist.')
        else:
            user.save()
        return redirect('customer_login')
    return render(request, "customer_signup.html")

def customer_login(request): 
    if request.method=="POST":
        try:
            e=request.POST['email'] 
            request.session['email']=e            
            p=request.POST['password']                       
            x=Customer.objects.get(email=e)                         
            if x.password==p:                
                return redirect('/customer_homepage')
            else:
                messages.warning(request, 'Please input correct password')                
        except:
            messages.warning(request,'Enter Username And Password.')
    return render(request, "customer_login.html")

def customer_homepage(request):
    location = Location.objects.all()
    return render(request, "customer_homepage.html",{'l':location})

def search_results(request):
    city = request.POST['city']    
    vehicles_list = []
    location = Location.objects.filter(city = city)
    print(location)
    for a in location:
        cars = Car.objects.filter(location=a)
        for car in cars:
            if car.is_available == True:
                vehicle_dictionary = {'name':car.name, 'id':car.id, 'image':car.image.url, 'city':car.location,'capacity':car.capacity}
                vehicles_list.append(vehicle_dictionary)
    request.session['vehicles_list'] = vehicles_list
    return render(request, "search_results.html")

def car_rent(request):
    id = request.POST['id']
    car = Car.objects.get(id=id)
    cost_per_day = int(car.rent)
    return render(request, 'car_rent.html', {'car':car, 'cost_per_day':cost_per_day})

def order_details(request):
    if request.session.has_key('email'):
        car_id = request.POST['id']
        email = request.session['email']
        user = Customer.objects.get(email=email)
        days = request.POST['days']
        car = Car.objects.get(id=car_id)
        if car.is_available:
            car_dealer = car.car_dealer
            rent = (int(car.rent))*(int(days))
            car_dealer.earnings += rent
            car_dealer.save()
            try:
                order = Order(car=car, dealer=car_dealer, customer=user, rent=rent, days=days)
                order.save()
            except:
                order = Order.objects.get(car=car, dealer=car_dealer, customer=user, rent=rent, days=days)
            car.is_available = False
            car.save()
            return render(request, "order_details.html", {'order':order})
    return render(request, "order_details.html")