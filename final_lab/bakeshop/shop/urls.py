from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'), 
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('order/', views.create_order, name='Orders'),

    #PRODUCT
    path('product/<int:pk>', views.product, name='product'),
    path('product/add_product', views.add_product, name='add_product'),
    path('product/<pk>/edit_product', views.edit_product, name='edit_product'),
    path('product/<pk>/del_product', views.del_product, name='del_product'),



    #CATEGORY
    path('category/<int:pk>', views.category, name='category'),
    path('category/add_category', views.add_category, name='add_category'),
    path('category/<pk>/edit_category', views.edit_category, name='edit_category'),
    path('category/<pk>/del_category', views.del_category, name="del_category"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    