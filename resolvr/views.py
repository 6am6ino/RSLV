from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, UserProfile  # Assuming you have a Case model
from .forms import UserRegistrationForm, CaseForm  # Assuming you have forms defined for signup and case creation
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import logout


@login_required
def dashboard(request):
    return render(request, 'customers/customer_dashboard.html')  # Render the dashboard template


def index(request):
    return render(request, 'index.html')  # Render the home page


def portfolio(request):
    return render(request, 'portfolio-details.html')  # Render the portfolio page


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('index')  # Redirect to a success page (adjust as needed)
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def contacts(request):
    return render(request, 'contacts.html')  # Render the contacts page


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            # Create a UserProfile instance for the new user (if needed)
            UserProfile.objects.create(user=user, email=form.cleaned_data['email'])

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})


def case_list(request):
    cases = Case.objects.all()  # Fetch all cases from the database
    return render(request, 'customers/case_list.html', {'cases': cases})  # Render case list


def create_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new case to the database
            return redirect('case_list')  # Redirect to case list after creation
    else:
        form = CaseForm()
    return render(request, 'customers/create_case.html', {'form': form})  # Render create case page


def case_detail(request, case_id):
    case = get_object_or_404(Case, id=case_id)  # Fetch the specific case or return a 404 error
    return render(request, 'customers/case_detail.html', {'case': case})  # Render case detail page


def arbitration_view(request):
    return render(request, 'arbitration.html')  # Render arbitration view


def service_details(request):
    return render(request, 'service-details.html')  # Render service details page


def starterpage(request):
    return render(request, 'starter-page.html')  # Render starter page


def base_view(request):
    return render(request, 'base.html')  # Render base view


def logout_view(request):
    logout(request)
    messages.info(request, 'You have logged out successfully.')
    return redirect('login')  # Redirects directly to the login page


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.role == 'customer':
                return redirect('customer_dashboard')  # URL name for customer dashboard
            elif user.role == 'mediator':
                return redirect('mediator_dashboard')  # URL name for mediator dashboard
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required
def customer_dashboard(request):
    return render(request, 'customers/customer_dashboard.html')


@login_required
def mediator_dashboard(request):
    return render(request, 'mediators/mediator_dashboard.html')
