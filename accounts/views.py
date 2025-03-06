from django.shortcuts import render, redirect
from .models import HotelUser, Hotelvendor,Hotel,Ameneties,HotelImages
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken,sendEmailToken ,sendOTPtoEmail
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
import random
from django.contrib.auth.decorators import login_required
from .utils import generateSlug
from django.http import HttpResponseRedirect

# Create your views here.
'''
def login_page(request):
    print('Inside login Page')

    return render(request,'login.html')
'''


def register(request):
    print('Inside register Page')
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(Q(email = email) | Q(phone_number=phone_number))
        
        if hotel_user.exists():
            messages.error(request , 'Account exists with email or phone number')
            return redirect('/register')
        
        hotel_user = HotelUser.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email,hotel_user.email_token)

        messages.success(request , 'Email Sent to your Email')
        return redirect('/register')

    return render(request,'register.html')
'''
def verify_email_token(request,token):
    try:
        hotel_user = HotelUser.objects.get(email_token = token)
        hotel_user.is_verified = True 
        hotel_user.save()
        messages.success(request , 'Email verified')
        return redirect('/login')

    except Exception as e:
        return HttpResponse('Invalid Token')

'''

def verify_email_token(request, token):
    try:
        # Check if token belongs to HotelUser
        user = HotelUser.objects.filter(email_token=token).first()
        if user:
            user.is_verified = True
            user.save()
            messages.success(request, 'Email verified successfully!')
            return redirect('/login')

        # Check if token belongs to Hotelvendor
        vendor = Hotelvendor.objects.filter(email_token=token).first()
        if vendor:
            vendor.is_verified = True
            vendor.save()
            messages.success(request, 'Vendor email verified successfully!')
            return redirect('/login-vendor')

        # If neither user nor vendor exists
        return HttpResponse('Invalid Token')

    except Exception as e:
        return HttpResponse('Error occurred: ' + str(e))


def login_page(request):
    print('Inside login Page')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email = email)
        
        if not hotel_user.exists():
            messages.error(request , 'No1 Account Found')
            return redirect('/login')
        
        if not hotel_user[0].is_verified:
            messages.success(request , 'ACCOUNT NOT VERIFIED')
            return redirect('/login')
        
        
        hotel_user = authenticate(username=hotel_user[0].username,password=password)

        if hotel_user:
            messages.success(request , 'Login successful')
            login(request,hotel_user)
            return redirect('/')
        
        messages.success(request , 'Invalid credentials')
        return redirect('/login')

    return render(request,'login.html')

def send_otp(request,email):
    hotel_user = HotelUser.objects.filter(email=email)
    if not hotel_user.exists():
        messages.warning(request,"No Account Found")
        return redirect('/login')
    otp = random.randint(1000,9999)
    hotel_user.update(otp = otp)
    sendOTPtoEmail(email,otp)

    return redirect(f'/verify-otp/{email}/')

def verify_otp(request,email):
    print("Received email in URL:", email)
    if request.method == "POST":
        otp = request.POST.get('otp')
        print("---otp---",otp)
        hotel_user = HotelUser.objects.get(email=email)

        if str(otp) == str(hotel_user.otp):
            print("-------Hi-------------")
            messages.success(request,"Login Success")
            login(request,hotel_user)
            return redirect('/login')
        
        messages.warning(request,"Wrong OTP")
        return redirect('/verify-otp/{email}/')
    
    return render(request,'verify_otp.html')


#####################################################################################################################################################

#---------------Login and register views for Vendor--------------
'''
def register_vendor(request):
    print('Inside register Page')
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(Q(email = email) | Q(phone_number=phone_number))
        
        if hotel_user.exists():
            messages.error(request , 'Account exists with email or phone number')
            return redirect('/register-vendor')
        
        hotel_user = Hotelvendor.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            business_name = business_name,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email,hotel_user.email_token)

        messages.success(request , 'Email Sent to your Email')
        return redirect('/register-vendor')

    return render(request,'vendor/register_vendor.html')


'''

def register_vendor(request):
    print('Inside register_vendor Page')

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        # ✅ Check if email or phone number already exists in Hotelvendor
        if Hotelvendor.objects.filter(Q(email=email) | Q(phone_number=phone_number)).exists():
            messages.error(request, 'Account already exists with this email or phone number.')
            return redirect('/register-vendor')

        # ✅ Set username as phone number (ensuring uniqueness)
        username = phone_number

        # ✅ Ensure username is unique
        if Hotelvendor.objects.filter(username=username).exists():
            messages.error(request, 'An account with this phone number already exists.')
            return redirect('/register-vendor')

        # ✅ Create the Hotelvendor instance
        vendor_user = Hotelvendor(
            username=username,  # This was missing in your original code
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            business_name=business_name,
            email_token=generateRandomToken()
        )
        vendor_user.set_password(password)  # ✅ Ensure password is hashed
        vendor_user.save()

        # ✅ Send email verification
        sendEmailToken(email, vendor_user.email_token)

        messages.success(request, 'Verification email has been sent. Please check your inbox.')
        return redirect('/register-vendor')

    return render(request, 'vendor/register_vendor.html')

'''

def login_vendor(request):
    print('Inside login Page')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = Hotelvendor.objects.filter(email = email)
        
        if not hotel_user.exists():
            messages.error(request , 'No1 Account Found')
            return redirect('/login-vendor')
        
        if not hotel_user[0].is_verified:
            messages.success(request , 'ACCOUNT NOT VERIFIED')
            return redirect('/login-vendor')
        
        
        hotel_user = authenticate(username=hotel_user[0].username,password=password)

        if hotel_user:
            messages.success(request , 'Login successful')
            login(request,hotel_user)
            return redirect('/dashboard')
        
        messages.success(request , 'Invalid credentials')
        return redirect('/login-vendor')

    return render(request,'vendor/login_vendor.html')

'''
'''
def login_vendor(request):
    print('Inside vendor login Page')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Attempting login for email: {email}")  # Debugging

        hotel_user = Hotelvendor.objects.filter(email=email).first()

        if not hotel_user:
            messages.error(request, 'No Account Found')
            print("No account found for this email!")  # Debugging
            return redirect('/login-vendor')

        if not hotel_user.is_verified:
            messages.error(request, 'ACCOUNT NOT VERIFIED')
            print("Account not verified!")  # Debugging
            return redirect('/login-vendor')

        # ✅ Correct authentication using email
        hotel_user = authenticate(request, email=email, password=password)

        if hotel_user:
            print(f"User {hotel_user.email} authenticated successfully!")  # Debugging
            messages.success(request, 'Login successful')
            login(request, hotel_user)
            return redirect('/dashboard')

        print("Invalid credentials!")  # Debugging
        messages.error(request, 'Invalid credentials')
        return redirect('/login-vendor')

    return render(request, 'vendor/login_vendor.html')
'''
'''
def login_vendor(request):
    print('Inside vendor login Page')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Attempting login for email: {email}")  # Debugging

        hotel_user = Hotelvendor.objects.filter(email=email).first()

        if not hotel_user:
            messages.error(request, 'No Account Found')
            print("No account found for this email!")  # Debugging
            return redirect('/login-vendor')

        if not hotel_user.is_verified:
            messages.error(request, 'ACCOUNT NOT VERIFIED')
            print("Account not verified!")  # Debugging
            return redirect('/login-vendor')

        # ✅ Authenticate using the correct field (username instead of email)
        authenticated_user = authenticate(request, username=hotel_user.username, password=password)

        if authenticated_user:
            print(f"User {authenticated_user.email} authenticated successfully!")  # Debugging
            messages.success(request, 'Login successful')
            login(request, authenticated_user)
            return redirect('/dashboard')

        print("Invalid credentials!")  # Debugging
        messages.error(request, 'Invalid credentials')
        return redirect('/login-vendor')

    return render(request, 'vendor/login_vendor.html')
'''


#from django.contrib.auth.hashers import check_password

'''
def login_vendor(request):
    print('Inside vendor login Page')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Attempting login for email: {email}")  # Debugging

        hotel_user = Hotelvendor.objects.filter(email=email).first()

        if not hotel_user:
            messages.error(request, 'No Account Found')
            print("No account found for this email!")  # Debugging
            return redirect('/login-vendor')

        if not hotel_user.is_verified:
            messages.error(request, 'ACCOUNT NOT VERIFIED')
            print("Account not verified!")  # Debugging
            return redirect('/login-vendor')

        # ✅ Manually check password since `authenticate()` does not work for Hotelvendor
        if check_password(password, hotel_user.password):
            print(f"User {hotel_user.email} authenticated successfully!")  # Debugging
            login(request, hotel_user)  # Log in manually
            messages.success(request, 'Login successful')
            return redirect('/dashboard')

        print("Invalid credentials!")  # Debugging
        messages.error(request, 'Invalid credentials')
        return redirect('/login-vendor')

    return render(request, 'vendor/login_vendor.html')
'''
'''
from django.contrib.auth.hashers import check_password

def login_vendor(request):
    print('Inside vendor login Page')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Attempting login for email: {email}")  # Debugging

        hotel_user = Hotelvendor.objects.filter(email=email).first()

        if not hotel_user:
            messages.error(request, 'No Account Found')
            print("No account found for this email!")  # Debugging
            return redirect('/login-vendor')

        if not hotel_user.is_verified:
            messages.error(request, 'ACCOUNT NOT VERIFIED')
            print("Account not verified!")  # Debugging
            return redirect('/login-vendor')

        # ✅ Manually check password since `authenticate()` does not work for Hotelvendor
        if check_password(password, hotel_user.password):
            print(f"User {hotel_user.email} authenticated successfully!")  # Debugging
            
            # ✅ Store vendor user in session
            request.session['vendor_id'] = hotel_user.id
            request.session['vendor_email'] = hotel_user.email
            request.session['vendor_authenticated'] = True  # Custom session flag

            messages.success(request, 'Login successful')
            return redirect('/dashboard')

        print("Invalid credentials!")  # Debugging
        messages.error(request, 'Invalid credentials')
        return redirect('/login-vendor')

    return render(request, 'vendor/login_vendor.html')
'''
from django.contrib.auth.hashers import check_password

from django.contrib.auth import get_user_model

def login_vendor(request):
    print('Inside vendor login Page')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Attempting login for email: {email}")  # Debugging

        hotel_user = Hotelvendor.objects.filter(email=email).first()

        if not hotel_user:
            messages.error(request, 'No Account Found')
            print("No account found for this email!")  # Debugging
            return redirect('/login-vendor')

        if not hotel_user.is_verified:
            messages.error(request, 'ACCOUNT NOT VERIFIED')
            print("Account not verified!")  # Debugging
            return redirect('/login-vendor')

        # ✅ Manually check password since `authenticate()` does not work for Hotelvendor
        if hotel_user.check_password(password):
            print(f"User {hotel_user.email} authenticated successfully!")  # Debugging
            request.session['vendor_id'] = hotel_user.id  # Store vendor in session
            login(request, hotel_user, backend='accounts.backends.VendorBackend')  # Specify backend
            messages.success(request, 'Login successful')
            return redirect('/dashboard')

        print("Invalid credentials!")  # Debugging
        messages.error(request, 'Invalid credentials')
        return redirect('/login-vendor')

    return render(request, 'vendor/login_vendor.html')



######################################################################
#-----------------DASHBOARD-----------------------------------------

'''
@login_required(login_url='login_vendor')
def dashboard(request):
    print('-------------------Hi-------------------')
    hotels = Hotel.objects.filter(hotel_owner=request.user)
    context = {'hotels': hotels}
    return render(request, 'vendor/vendor_dashboard.html', context)
'''

def dashboard(request):
    print('-------------------Hi-------------------')

    # ✅ Check if vendor is authenticated
    if not request.session.get('vendor_authenticated', False):
        messages.error(request, "You must be logged in as a vendor.")
        return redirect('/login-vendor')

    # ✅ Retrieve vendor details from session
    vendor_id = request.session.get('vendor_id')
    vendor_user = Hotelvendor.objects.filter(id=vendor_id).first()

    if not vendor_user:
        messages.error(request, "Vendor not found.")
        return redirect('/login-vendor')

    hotels = Hotel.objects.filter(hotel_owner=vendor_user)
    context = {'hotels': hotels, 'vendor_user': vendor_user}
    
    return render(request, 'vendor/vendor_dashboard.html', context)

'''
@login_required(login_url='login_vendor')   
def add_hotel(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties=request.POST.get('ameneties')
        hotel_price = request.POST.get('hotel_price')
        hotel_office_price = request.POST.get('hotel_office_price')
        hotel_location = request.POST.get('hotel_location')
        hotel_slug = generateSlug(hotel_name)

        Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description= hotel_description,
            hotel_price = hotel_description,
            hotel_office_price = hotel_office_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug
        )
       #return redirect(request,'/dashboard')
    return redirect(request,'vendor/add_hotel.html')

'''

'''
@login_required(login_url='login_vendor')
def add_hotel(request):
    print("-----------inside add hotel--------------")
    if request.method == "POST":
        hotel_name = request.POST.get("hotel_name")
        hotel_description = request.POST.get("hotel_description")
        ameneties = request.POST.getlist("amenties")
        hotel_price = request.POST.get("hotel_price")
        hotel_offer_price = request.POST.get("hotel_offer_price")
        hotel_location = request.POST.get("hotel_location")
        hotel_slug = generateSlug(hotel_name)


        #hotel_vendor= Hotelvendor.objects.get(id=request.user.id)

        try:
            hotel_vendor = Hotelvendor.objects.get(username=request.user.username)
        except Hotelvendor.DoesNotExist:
            messages.error(request, "Vendor account not found.")
            return redirect('/add-hotel')
        
        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor
        )

        for ameneti in ameneties:
            ameneti = Ameneties.objects.get(id= ameneti)
            hotel_obj.ameneties.add(ameneti)
            hotel_obj.save()

        messages.success(request,"Hotel Created")
        return redirect('/add-hotel')

    ameneties = Ameneties.objects.all()
    return render(request,'vendor/add_hotel.html', context={'ameneties': ameneties})

'''
@login_required(login_url='/login-vendor')
def add_hotel(request):
    print("-----------inside add hotel--------------")
    if request.method == "POST":
        hotel_name = request.POST.get("hotel_name")
        hotel_description = request.POST.get("hotel_description")
        ameneties = request.POST.getlist("amenties")
        hotel_price = request.POST.get("hotel_price")
        hotel_offer_price = request.POST.get("hotel_offer_price")
        hotel_location = request.POST.get("hotel_location")
        hotel_slug = generateSlug(hotel_name)

        # Get vendor from session
        vendor_id = request.session.get('vendor_id')
        if not vendor_id:
            messages.error(request, "Vendor not logged in.")
            return redirect('/login-vendor')

        try:
            hotel_vendor = Hotelvendor.objects.get(id=vendor_id)
        except Hotelvendor.DoesNotExist:
            messages.error(request, "Vendor account not found.")
            return redirect('/login-vendor')

        hotel_obj = Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_description=hotel_description,
            hotel_price=hotel_price,
            hotel_offer_price=hotel_offer_price,
            hotel_location=hotel_location,
            hotel_slug=hotel_slug,
            hotel_owner=hotel_vendor
        )

        for ameneti in ameneties:
            ameneti_obj = Ameneties.objects.get(id=ameneti)
            hotel_obj.ameneties.add(ameneti_obj)

        hotel_obj.save()

        messages.success(request, "Hotel Created")
        return redirect('/add-hotel')

    ameneties = Ameneties.objects.all()
    return render(request, 'vendor/add_hotel.html', context={'ameneties': ameneties})


@login_required(login_url='login_vendor')
def upload_images(request,slug):
    print("-----------inside upload images--------------")
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    if request.method == "POST":
        image = request.FILES['image']
        print(image)
        HotelImages.objects.create(
            hotel = hotel_obj,
            image = image
              )
       
        return HttpResponseRedirect(request.path_info)
    hotel_images = HotelImages.objects.filter(hotel = hotel_obj)
    return render(request,'vendor/upload_images.html',context={'images': hotel_images})


@login_required(login_url='login_vendor')
def upload_images(request, slug):
    print("-----------inside upload images--------------")
    
    try:
        hotel_obj = Hotel.objects.get(hotel_slug=slug)
    except Hotel.DoesNotExist:
        messages.error(request, "Hotel not found!")
        return redirect('/dashboard')

    if request.method == "POST":
        image = request.FILES.get('image')  # Use .get() to prevent crashes if no file is selected
        if image:
            print(f"Uploading image: {image}")
            HotelImages.objects.create(hotel=hotel_obj, image=image)
            return HttpResponseRedirect(request.path_info)

    # Retrieve only images linked to this specific hotel
    hotel_images = HotelImages.objects.filter(hotel=hotel_obj)
    print(f"Total images for {hotel_obj.hotel_name}: {hotel_images.count()}")  # Debugging

    return render(request, 'vendor/upload_images.html', context={'images': hotel_images})

@login_required(login_url='login_vendor')
def delete_image(request, id):
    print(id)
    print("#######")
    hotel_image = HotelImages.objects.get(id = id)
    hotel_image.delete()
    messages.success(request, "Hotel Image deleted")
    return redirect('/dashboard')

@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not authorized")
    
    if request.method == "POST":
        hotel_name = request.POST.get("hotel_name")
        hotel_description = request.POST.get("hotel_description")
        hotel_price = request.POST.get("hotel_price")
        hotel_offer_price = request.POST.get("hotel_offer_price")
        hotel_location = request.POST.get("hotel_location")
        
        hotel_obj.hotel_name =  hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        messages.success(request,"Hotel data updated")

        return HttpResponseRedirect(request.path_info)
    
    ameneties = Ameneties.objects.all()
    return render(request,'vendor/edit_hotel.html',context = {'hotel': hotel_obj,'ameneties': ameneties})

def logout_view(request):
    logout(request)
    messages.success(request,'Logout success')
    return redirect('/login')
