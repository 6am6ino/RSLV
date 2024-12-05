from django.urls import path
from .views import (
    index,
    login_view,
    dashboard,
    contacts,
    portfolio,
    logout_view,
    signup,
    dashboard,
    case_list,
    create_case,
    case_detail, arbitration_view, service_details, starterpage, base_view,
)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('customer/dashboard/', dashboard, name='customer_dashboard'),  # If using your own login view
    path('portfolio/', portfolio, name='portfolio'),
    path('contacts/', contacts, name='contacts'),
    path('signup/', signup, name='signup'),
    path('customer/dashboard/', dashboard, name='customer_dashboard'),
    path('customer/cases/', case_list, name='case_list'),
    path('customer/cases/create/', create_case, name='create_case'),
    path('customer/cases/<int:case_id>/', case_detail, name='case_detail'),
    path('arbitration/', arbitration_view, name='arbitration'),
    path('service-details/', service_details, name='service_details'),
    path('logout/', logout_view, name='logout'),
   path('starterpage/', starterpage, name='starterpage'),
    path('base/', base_view, name='base'),
]
