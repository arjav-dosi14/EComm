from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from main.models import Category, Product, UserProfile, Order, OrderItem
from main.forms import UserRegisterForm, UserProfileForm, ProductForm, OrderForm

# Helper function for cart details
def get_cart_details(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0.00')
    
    for product_id_str, quantity in list(cart.items()):
        try:
            product = Product.objects.get(id=int(product_id_str))
            item_total = product.price * quantity
            subtotal += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
        except (Product.DoesNotExist, ValueError):
            # Clean up invalid product IDs
            if product_id_str in cart:
                del cart[product_id_str]
                request.session.modified = True
            
    # Calculate totals
    # Free shipping above ₹4999, else ₹100 shipping
    shipping = Decimal('100.00') if subtotal > 0 and subtotal < 4999 else Decimal('0.00')
    if subtotal == 0:
        shipping = Decimal('0.00')
        
    discount = Decimal('0.00')
    coupon_code = request.session.get('coupon', None)
    if coupon_code == 'SHOP20' and subtotal > 0:
        discount = subtotal * Decimal('0.20')  # 20% coupon discount
    
    gst = subtotal * Decimal('0.02')  # 2% GST
    total_amount = subtotal + shipping + gst - discount
    
    return {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'discount': discount,
        'gst': gst,
        'total_amount': total_amount,
        'total_count': sum(cart.values()),
        'coupon_code': coupon_code
    }

# Catalog views
def home(request):
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(is_featured=True)[:4]
    trending_products = Product.objects.filter(is_trending=True)[:4]
    cart_details = get_cart_details(request)
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'trending_products': trending_products,
        'cart_count': cart_details['total_count']
    }
    return render(request, 'home.html', context)

def categories(request):
    categories_list = Category.objects.all()
    cart_details = get_cart_details(request)
    context = {
        'categories_list': categories_list,
        'cart_count': cart_details['total_count']
    }
    return render(request, 'categories.html', context)

def products(request, category_slug=None):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    categories_all = Category.objects.all()
    current_category = None
    
    # Base queryset
    products_list = Product.objects.all()
    
    # Category filter
    selected_categories = request.GET.getlist('category')
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        if category_slug not in selected_categories:
            selected_categories = [category_slug] + selected_categories
            
    if selected_categories:
        products_list = products_list.filter(category__slug__in=selected_categories)
        
    # Search filter
    query = request.GET.get('q', '')
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    # Price range filter
    price_filter = request.GET.get('price', '')
    if price_filter == 'under_500':
        products_list = products_list.filter(price__lt=500)
    elif price_filter == '500_2000':
        products_list = products_list.filter(price__gte=500, price__lte=2000)
    elif price_filter == '2000_5000':
        products_list = products_list.filter(price__gte=2000, price__lte=5000)
    elif price_filter == 'above_5000':
        products_list = products_list.filter(price__gt=5000)
        
    # Sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')
    elif sort_by == 'newest':
        products_list = products_list.order_by('-created_at')
    elif sort_by == 'name_asc':
        products_list = products_list.order_by('name')
    else:
        # Default sorting by rating (popularity)
        products_list = products_list.order_by('-rating')
        
    # Get total count before pagination
    total_count = products_list.count()
    
    # Pagination (9 products per page)
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    try:
        products_page = paginator.page(page_number)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
        
    cart_details = get_cart_details(request)
    
    # Recently Viewed from session
    rv_ids = request.session.get('recently_viewed', [])
    recently_viewed_products = Product.objects.filter(id__in=rv_ids)[:4]
    
    # Construct query parameters to persist filter settings across pagination
    query_dict = request.GET.copy()
    if 'page' in query_dict:
        del query_dict['page']
    page_query_params = query_dict.urlencode()
    
    context = {
        'products': products_page,
        'categories_all': categories_all,
        'selected_categories': selected_categories,
        'price_filter': price_filter,
        'sort_by': sort_by,
        'query': query,
        'cart_count': cart_details['total_count'],
        'recently_viewed': recently_viewed_products,
        'total_count': total_count,
        'current_category': current_category,
        'page_query_params': page_query_params
    }
    return render(request, 'products.html', context)

def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_details = get_cart_details(request)
    
    # Store recently viewed in session
    rv_ids = request.session.get('recently_viewed', [])
    if product.id in rv_ids:
        rv_ids.remove(product.id)
    rv_ids.insert(0, product.id)
    request.session['recently_viewed'] = rv_ids[:10]  # Keep last 10
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    if len(related_products) < 4:
        extra_products = Product.objects.exclude(category=product.category).exclude(id=product.id)[:4-len(related_products)]
        related_products = list(related_products) + list(extra_products)
        
    context = {
        'product': product,
        'related_products': related_products,
        'cart_count': cart_details['total_count']
    }
    return render(request, 'product_details.html', context)

# Auth Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
            
    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            messages.success(request, "Registration successful. Welcome to ShopSphere!")
            return redirect('home')
        else:
            errors = form.errors.as_data()
            err_msg = ""
            for field, err_list in errors.items():
                for err in err_list:
                    err_msg += f"{field.capitalize()}: {err.message} "
            return render(request, 'register.html', {'error': err_msg or "Form validation failed"})
            
    return render(request, 'register.html')

def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = UserProfileForm(instance=user_profile)
        
    orders_count = request.user.orders.count()
    points = user_profile.points
    cart_details = get_cart_details(request)
    
    context = {
        'profile': user_profile,
        'form': form,
        'orders_count': orders_count,
        'points': points,
        'cart_count': cart_details['total_count']
    }
    return render(request, 'profile.html', context)

# Shopping Cart Views
def cart(request):
    cart_details = get_cart_details(request)
    
    # Handle Coupon application
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'apply_coupon':
            code = request.POST.get('coupon_code', '').strip().upper()
            if code == 'SHOP20':
                request.session['coupon'] = code
                messages.success(request, "Coupon applied successfully! 20% discount added.")
            else:
                messages.error(request, "Invalid coupon code.")
            return redirect('cart')
            
    # Recommended Products
    recommended = Product.objects.all().order_by('-rating')[:4]
    
    context = {
        'cart_items': cart_details['cart_items'],
        'subtotal': cart_details['subtotal'],
        'shipping': cart_details['shipping'],
        'discount': cart_details['discount'],
        'gst': cart_details['gst'],
        'total_amount': cart_details['total_amount'],
        'cart_count': cart_details['total_count'],
        'coupon_code': cart_details['coupon_code'],
        'recommended': recommended
    }
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.GET.get('qty', 1))
    
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + qty
    
    request.session['cart'] = cart
    request.session.modified = True
    
    messages.success(request, f"Added {product.name} to cart.")
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item removed from cart.")
    return redirect('cart')

def update_cart_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            if action == 'increase':
                cart[product_id_str] += 1
            elif action == 'decrease':
                cart[product_id_str] -= 1
                if cart[product_id_str] <= 0:
                    del cart[product_id_str]
            request.session['cart'] = cart
            request.session.modified = True
            
            cart_details = get_cart_details(request)
            # Find item price
            product = get_object_or_404(Product, id=int(product_id))
            item_total = product.price * cart.get(product_id_str, 0)
            
            return JsonResponse({
                'success': True,
                'quantity': cart.get(product_id_str, 0),
                'item_total': float(item_total),
                'subtotal': float(cart_details['subtotal']),
                'shipping': float(cart_details['shipping']),
                'discount': float(cart_details['discount']),
                'gst': float(cart_details['gst']),
                'total_amount': float(cart_details['total_amount']),
                'cart_count': cart_details['total_count']
            })
            
    return JsonResponse({'success': False})

# Checkout & Checkout Processing
@login_required
def checkout(request):
    cart_details = get_cart_details(request)
    if not cart_details['cart_items']:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')
        
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart_details['total_amount']
            order.save()
            
            # Save items
            for item in cart_details['cart_items']:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )
                # Deduct stock
                item['product'].stock = max(0, item['product'].stock - item['quantity'])
                item['product'].save()
                
            # Reward loyalty points (1 point per 10 rupees spent)
            points_gained = int(order.total_amount // 10)
            profile.points += points_gained
            profile.save()
            
            # Clear Cart
            request.session['cart'] = {}
            if 'coupon' in request.session:
                del request.session['coupon']
            request.session.modified = True
            
            messages.success(request, f"Order placed successfully! Gained {points_gained} loyalty points.")
            return redirect('history')
        else:
            messages.error(request, "Failed to place order. Please review form entries.")
    else:
        # Prepopulate form with user profile address info
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
            'phone': profile.phone_number,
            'address': profile.address_line1,
            'city': profile.city,
            'state': profile.state,
            'zip_code': profile.zip_code,
            'country': profile.country
        }
        form = OrderForm(initial=initial_data)
        
    context = {
        'form': form,
        'cart_items': cart_details['cart_items'],
        'subtotal': cart_details['subtotal'],
        'shipping': cart_details['shipping'],
        'discount': cart_details['discount'],
        'gst': cart_details['gst'],
        'total_amount': cart_details['total_amount'],
        'cart_count': cart_details['total_count']
    }
    return render(request, 'checkout.html', context)

@login_required
def history(request):
    orders = request.user.orders.all().order_by('-created_at')
    cart_details = get_cart_details(request)
    
    # Calculate stats
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    processing = orders.filter(status='Processing').count()
    cancelled = orders.filter(status='Cancelled').count()
    
    # Buy Again items
    buy_again = Product.objects.all().order_by('?')[:4]
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'processing': processing,
        'cancelled': cancelled,
        'buy_again': buy_again,
        'cart_count': cart_details['total_count']
    }
    return render(request, 'history.html', context)

# Static templates views
def about(request):
    cart_details = get_cart_details(request)
    return render(request, 'about.html', {'cart_count': cart_details['total_count']})

def faq(request):
    cart_details = get_cart_details(request)
    return render(request, 'faq.html', {'cart_count': cart_details['total_count']})

def contact(request):
    cart_details = get_cart_details(request)
    return render(request, 'contact.html', {'cart_count': cart_details['total_count']})

def notfound(request):
    cart_details = get_cart_details(request)
    return render(request, 'notfound.html', {'cart_count': cart_details['total_count']})


# --- Custom Admin Dashboard Views ---
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    products = Product.objects.all().order_by('-created_at')
    orders = Order.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Stats
    total_sales = sum(o.total_amount for o in orders.filter(status='Delivered'))
    pending_orders = orders.filter(status='Processing').count()
    total_products = products.count()
    
    context = {
        'products': products,
        'orders': orders,
        'categories': categories,
        'total_sales': total_sales,
        'pending_orders': pending_orders,
        'total_products': total_products,
        'cart_count': 0
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Default category specific image mapping if empty
            if not product.image_url and not product.image:
                category_slug = product.category.slug
                defaults = {
                    'electronics': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDSwDRJxNFmK069KXM20MxZXW3RQoYzj3zoD7cQ9DF5uGFqh9jwPspob04eBJ7_KV41WINsHlkEqUvjgbrffp6DB3hW1L69ZaKCNiRUu6tYAsSEpUFVx1vPMnnS1M6J2wx37ydAch1-K4meCKB-ysEwH27FaRsC3ctUmPfNRGQFNYa1K2rcGxVuRvFvXRrokZjheKAmZX3W9XlGIBrv3l0pDSh1M_my_i70pWMC7T0PbL6owWHJLUGD-1JK50NSqnWsEykhAq8Sr3Lf',
                    'fashion': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCSQ4DMCqGq0nceqN_IlHrEhxsrQSKbwm34g15QYulOTQxfu8ORbNLwagokUpX-QV2ia5SKsqwoGwWcZMmsnP_BbKD_4nCK99HCDxJjfoAA6gu1x4TTdLmEvYMpXAOLSMtAJxjEjDASfb2RoB5NnErYHELVLKc-iz0WM79fePPJK6w_tCpfWw2DxPgRFbLviJqLM-KHgbT11bouPgHK-Wfa1xplleeJUjYxH3CyCpVyUafRDooQ-GzkQg8ZfHw2s8AQ4EDfJ4JBUWUT',
                    'home-kitchen': 'https://lh3.googleusercontent.com/aida-public/AB6AXuB_0nUQivX2McLeFSu6KTZBbnOTRFa2cukaJazmeJCqLB_695v_VYnWmYTr7szkR-L4f3Mo3yXCvmsppyj27QiSjxKrVXUcKlRMu3TL84xLa_3H94ffawod5BfoHexOgjXIBCGc0Bi3sPbxmgOYDseUKQlKbCSHLnFFJMnuuQkn71055DPn7Yg4uOKJ5ThkajQ0sSO0XNEQAG5R6sxxfl9kOTwZqCJfBmkD2WvdZAhV2G3jhAYwY7asFEsUumZ3RqTCxNSQ2rd9D6hm',
                    'beauty': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBTsZ4r9dt96r1Flrn6m2dUO7GBQg7Gjwq5skhVWgQvLh_wu6QV5DaztTlFg_j-F9oELxnSIvy2903sAIBmJIZHu3naL6fnxiwsNie-T6OrcqTZugMGdmMdtFp-MzVp4olArH_sU-8EDvTQaNinjm9ci6ovcFvfHmfx3vWFhKeUkRxY2CRWC8__jU5Ow0JjkW-GAm8fv5FAnhnNZbfM-i3A1PZvB762aGeIFs-n7nxjDuonHm4tuFLcK4hBURngt4aW0ZqThNoi9Ajf',
                    'sports': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCBWGQf--EAvk6i45s5J9ftt1Zn0LLkg_WvK3H5_UlU1VIDLSoFPmHpIhDL7mezQzbPJqigCby_lwC_vAxDwaiRlV7WPe1_AfxeXkXMtTEwd0f5q3_atzZUfdCwfOLDDdE9nv90fBIX8LFJCAreS7RZxAcmEystDIRPtoVklSlOM467fBtshC3LmDKSIubLYEMdzi9AhU_f1mMkB0vGmo5rWsHQD-zqQ3nW3eZd_jj-gLtWmItneVuuxVz3gVT10NNPAGrtDJk1wnQL',
                    'accessories': 'https://lh3.googleusercontent.com/aida-public/AB6AXuACIrzz2wR40T2RAoFIHBEcb_Cks050yWfNg9V9vzSy9aKHDtb4tUS7PXYLjLvTXHsvOo58BsWM3b-AbXygqRkCgwR5DrflEQzpihibcv0DOVejPwqjM3cGjxmJMgA_EYIyJX1MBAQd1NMygSjJ83XcRFgpDcMxwop2uCKZnxNeG0Tglxm5O4ohaY-et5j_BM3DigxHC-3eMgZh3GLJygg0OwZg8Wu_pO2rgRGryp94mOz6PiJZ-kZGeTCLczyQ_obEU5LYMsAq1L01'
                }
                product.image_url = defaults.get(category_slug, defaults['electronics'])
            product.save()
            messages.success(request, f"Product {product.name} added successfully!")
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'admin_product_form.html', {'form': form, 'title': 'Add Product'})

@user_passes_test(lambda u: u.is_staff)
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product {product.name} updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_product_form.html', {'form': form, 'title': 'Edit Product'})

@user_passes_test(lambda u: u.is_staff)
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product {name} deleted successfully.")
        return redirect('admin_dashboard')
    return render(request, 'admin_product_delete.html', {'product': product})

@user_passes_test(lambda u: u.is_staff)
def admin_order_status_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {status}.")
        else:
            messages.error(request, "Invalid status choice.")
    return redirect('admin_dashboard')