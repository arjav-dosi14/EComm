from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Product, Category, UserProfile, Order, OrderItem

class CheckoutFlowTestCase(TestCase):
    def setUp(self):
        # Create category and product
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=self.category,
            price=100.00,
            stock=10
        )
        self.client = Client()

    def test_registration_creates_profile(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNotNone(user.profile)

    def test_checkout_flow_new_user(self):
        self.client.post(reverse('register'), {
            'username': 'checkoutuser',
            'email': 'checkoutuser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123'
        })
        
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        
        session = self.client.session
        self.assertIn(str(self.product.id), session.get('cart', {}))
        
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('checkout'), {
            'full_name': 'Checkout User',
            'email': 'checkoutuser@example.com',
            'phone': '1234567890',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
            'country': 'India',
            'delivery_method': 'Standard',
            'payment_method': 'Card'
        })
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(username='checkoutuser')
        self.assertEqual(Order.objects.filter(user=user).count(), 1)
        
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.points, 20)

    def test_checkout_for_user_without_profile(self):
        user = User.objects.create_user(username='noprofileuser', email='no@example.com', password='password')
        UserProfile.objects.filter(user=user).delete()
        
        user = User.objects.get(username='noprofileuser')
        self.assertFalse(hasattr(user, 'profile'))
        
        self.client.login(username='noprofileuser', password='password')
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        
        response = self.client.post(reverse('checkout'), {
            'full_name': 'No Profile User',
            'email': 'no@example.com',
            'phone': '1234567890',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
            'country': 'India',
            'delivery_method': 'Standard',
            'payment_method': 'Card'
        })
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(username='noprofileuser')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.points, 20)

class ProductBrowsingTestCase(TestCase):
    def setUp(self):
        self.cat1 = Category.objects.create(name="Electronics", slug="electronics")
        self.cat2 = Category.objects.create(name="Books", slug="books")
        
        self.p1 = Product.objects.create(
            name="Smart Phone",
            slug="smart-phone",
            category=self.cat1,
            price=15000.00,
            rating=4.5,
            stock=10
        )
        self.p2 = Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.cat1,
            price=50000.00,
            rating=4.8,
            stock=5
        )
        self.p3 = Product.objects.create(
            name="Programming Book",
            slug="programming-book",
            category=self.cat2,
            price=600.00,
            rating=4.2,
            stock=20
        )
        self.client = Client()

    def test_category_page_renders(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Electronics")
        self.assertContains(response, "Books")

    def test_category_products_route(self):
        response = self.client.get(reverse('category_products', args=['electronics']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smart Phone")
        self.assertContains(response, "Laptop")
        self.assertNotContains(response, "Programming Book")

    def test_search_filter(self):
        response = self.client.get(reverse('products') + '?q=Laptop')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
        self.assertNotContains(response, "Smart Phone")

    def test_price_filter(self):
        # under 500
        response = self.client.get(reverse('products') + '?price=under_500')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Smart Phone")

        # 500_2000
        response = self.client.get(reverse('products') + '?price=500_2000')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Programming Book")
        self.assertNotContains(response, "Laptop")

    def test_sorting(self):
        # price low to high
        response = self.client.get(reverse('products') + '?sort=price_asc')
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'].object_list)
        self.assertEqual(products[0], self.p3) # 600.00
        self.assertEqual(products[1], self.p1) # 15000.00
        self.assertEqual(products[2], self.p2) # 50000.00

        # price high to low
        response = self.client.get(reverse('products') + '?sort=price_desc')
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'].object_list)
        self.assertEqual(products[0], self.p2) # 50000.00
        self.assertEqual(products[1], self.p1) # 15000.00
        self.assertEqual(products[2], self.p3) # 600.00

        # name a-z
        response = self.client.get(reverse('products') + '?sort=name_asc')
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'].object_list)
        self.assertEqual(products[0], self.p2) # Laptop
        self.assertEqual(products[1], self.p3) # Programming Book
        self.assertEqual(products[2], self.p1) # Smart Phone

class OrderHistoryFallbackTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Smart Phone",
            slug="smart-phone",
            category=self.category,
            price=15000.00,
            stock=10
        )
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.order = Order.objects.create(
            user=self.user,
            full_name="Test User",
            email="test@example.com",
            phone="1234567890",
            address="123 Test St",
            city="Test City",
            state="Test State",
            zip_code="12345",
            country="India",
            total_amount=15000.00
        )
        self.item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=15000.00,
            quantity=1
        )
        self.client = Client()

    def test_order_history_with_deleted_product(self):
        # Authenticate user
        self.client.login(username='testuser', password='password')
        
        # Delete the product associated with order item
        self.product.delete()
        
        # Access order history page
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        
        # Verify it displays fallback name instead of crashing
        self.assertContains(response, "Deleted Product")


