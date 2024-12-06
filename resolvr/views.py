from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, UserProfile, Arbitrator, Customer  # Import necessary models
from .forms import UserRegistrationForm, CaseForm, LoginForm, ArbitratorForm  # Import forms
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model


@login_required
def dashboard(request):
    return render(request, 'customers/customer_dashboard.html')  # Render the dashboard template


def index(request):
    return render(request, 'index.html')  # Render the home page


def portfolio(request):
    return render(request, 'portfolio-details.html')  # Render the portfolio page


def contacts(request):
    return render(request, 'contacts.html')  # Render the contacts page

def signup(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user to database with hashed password
            # Create UserProfile after saving the user
            UserProfile.objects.create(user=user, email=form.cleaned_data['email'])  # This will now be a CustomUser instance

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})

def case_list(request):
    """List all cases."""
    cases = Case.objects.all()  # Fetch all cases from the database
    return render(request, 'customers/case_list.html', {'cases': cases})  # Render case list


def create_case(request):
    """Create a new case."""
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.created_by = request.user  # Set the created_by field to the current user
            case.save()  # Save the new case to the database
            messages.success(request, 'Case created successfully.')
            return redirect('case_list')  # Redirect to case list after creation
    else:
        form = CaseForm()

    return render(request, 'customers/create_case.html', {'form': form})  # Render create case page


def case_detail(request, case_id):
    """Display details of a specific case."""
    case = get_object_or_404(Case, id=case_id)  # Fetch specific case or return a 404 error
    return render(request, 'customers/case_detail.html', {'case': case})  # Render case detail page


def arbitration_view(request):
    """Render arbitration view."""
    return render(request, 'arbitration.html')  # Render arbitration view


def service_details(request):
    """Render service details page."""
    return render(request, 'service-details.html')  # Render service details page


def starterpage(request):
    """Render starter page."""
    return render(request, 'starter-page.html')  # Render starter page


def base_view(request):
    """Render base view."""
    return render(request, 'base.html')  # Render base view


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have logged out successfully.')
    return redirect('login')  # Redirects to the login page


def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back {user.username}!')
                return redirect('customer_dashboard')  # Redirect based on role or dashboard
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def customer_dashboard(request):
    """Render customer dashboard."""
    return render(request, 'customers/customer_dashboard.html')


@login_required
def mediator_dashboard(request):
    """Render mediator dashboard."""
    return render(request, 'mediators/mediator_dashboard.html')


def register_arbitrator(request):
    """Register a new arbitrator."""
    if request.method == 'POST':
        form = ArbitratorForm(request.POST)
        if form.is_valid():
            arbitrator = form.save(commit=False)
            arbitrator.user.set_password(form.cleaned_data['user'].password)  # Hash the password for the user
            arbitrator.user.save()
            arbitrator.save()  # Save the Arbitrator instance
            messages.success(request, "Arbitrator registered successfully.")
            return redirect('login')  # Redirect after successful registration
    else:
        form = ArbitratorForm()

    return render(request, 'arbitration.html', {'form': form})  # Adjust template name as needed


def register_customer(request):
    """Register a new customer."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Customer.objects.create(user=user)  # Create a Customer instance
            messages.success(request, "Customer registered successfully.")
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration.html', {'form': form})