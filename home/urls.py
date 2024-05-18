from django.contrib.auth import views as auth_views
from django.urls import path 
from . import views 
 
urlpatterns = [ 
    path('', views.product_list, name='product_list'), 
    path('product/<int:product_id>/', views.product_detail, name='product_detail'), 
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'), 
    path('view_cart/', views.view_cart, name='view_cart'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('update_booking/<int:pk>/',views.update_booking, name='update_booking'),
    path('delete_booking/<int:pk>/',views.delete_booking, name='delete_booking'),
]