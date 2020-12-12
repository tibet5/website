from django.urls import path
from . import views

app_name = 'volunteers'
urlpatterns = [
    path('chef-application', views.ChefApplicationView.as_view(), name='chef_application'),
    path('chef-application-received', views.ChefApplicationReceivedView.as_view(), name='chef_application_received'),
    path('chef-signup', views.ChefSignupView.as_view(), name='chef_signup'),
    path('chef-list', views.ChefIndexView.as_view(), name='chef_list'),
    path('delivery-application', views.DeliveryApplicationView.as_view(), name='delivery_application'),
    path('delivery-application-received', views.DeliveryApplicationReceivedView.as_view(), name='delivery_application_received'),
    path('delivery-signup', views.MealDeliverySignupView.as_view(), name='delivery_signup_meals'),
    path('delivery-signup-groceries', views.GroceryDeliverySignupView.as_view(), name='delivery_signup_groceries'),
    path('delivery-list', views.DeliveryIndexView.as_view(), name='delivery_list'),
    path('volunteer-centre', views.VolunteerResourcesView.as_view(), name='volunteer_centre'),
]
