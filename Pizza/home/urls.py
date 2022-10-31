from django.urls import path
from . views import*

urlpatterns = [
    path('',home,name='home'),
    path('Add_Cart/<pizza_uid>',Add_Cart,name='Add_Cart'),
    path("singup",handelsingup,name='singup'),
    path('login/',handlogin,name='login'),
    path('logout/',handellogout,name='logout'),
    path('cart/',cart,name='cart'),
    path('order/',order,name='order'),
    path('remove_cart_item/<cart_item_uid>',remove_cart_item,name='remove_cart_item'),
     path('success/',success,name='success'),

]
