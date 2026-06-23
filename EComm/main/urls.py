from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('products/category/<slug:category_slug>/', views.products, name='category_products'),
    path('products/<slug:slug>/', views.product_details, name='product_details'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('notfound/', views.notfound, name='notfound'),
    
    # Custom admin routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/product/add/', views.admin_product_add, name='admin_product_add'),
    path('admin-dashboard/product/edit/<int:pk>/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-dashboard/product/delete/<int:pk>/', views.admin_product_delete, name='admin_product_delete'),
    path('admin-dashboard/order/<int:pk>/status/', views.admin_order_status_update, name='admin_order_status_update'),
]
