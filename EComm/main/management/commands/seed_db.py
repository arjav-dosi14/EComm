from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Category, Product

class Command(BaseCommand):
    help = "Seeds initial categories and products into the database"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing products and categories...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Seeding categories...")
        categories_data = [
            {
                "name": "Electronics",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuB-XimaHyHCmnjO-CFebngNNJgr_suQAYeCUyv6o1tqteuhoPRjQYMwi-roERcRlmDuPvyCkr91nFf-Bm4ttUBvHBXxcLeua42qXta2DNqcBoh4geiCnvM6jG_r7vJYrlFCQQ5oPPovk-OQubOGkSF8m0iYBBPC_IDaZMdjw1tftqPj7gnJP5NJw41jbsWFkY65lqDfPugoWCmYt_mD9UYMhVTNZhW1yfSCd2lzdbe_BmChafISNl7NDp2cHrN_6LgtSGD1tWJcua4",
                "description": "Laptops, phones, and smart home tech."
            },
            {
                "name": "Fashion",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuAABNtTC4wXaRpCYrTbHLDOgjt53rOkKx-QG6xw2upGX2dIIFYLuebCveW6t0FAXvnLZvHstVLoHv2Y1rFi1sRqXaoMErSLDdT9ruyq7ef3c6eHrdBN9CRk9M1PndDYh4lZIQhbwdRMab4QgE2YBfar7ZjpamZYJmTNOCCMAP0eBjr-OwwDmxsgyeQmgu9a7pvuQkxXC0Izx4Qdra3JfuCtO00GD3hgCjGI5xmJo-rchF1Hg_DsHCtmIlds1bpmZ1hpEeya7KdNAoU",
                "description": "Clothing, shoes, and accessories."
            },
            {
                "name": "Home & Kitchen",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBcuC9n48n9QefB_MoqPG6ZWrGdPBpyUszpHINn9pH8h3Ljrr32vlZUQ3RZGeWGYwddgi3EvqqtSvUGH1R7N2CPu_GsnKciKQmvCKhTLn8raVkJIDRtzqDWEPLn8UGjebeQ7LVV3xM6O7BsNoLkzGJXluyJzGHIOxQtGXSQM_lHcvpFXouVJqsZsZ3dVB-64f-TlhHSP_5Krz16NvBKeqlezHtF9FoPuDx5ZgazSDmnRExHxkx2oHjZHVVqGAVCmPrjYv2jhvI_D_E",
                "description": "Kitchenware, decor, and furniture."
            },
            {
                "name": "Beauty",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBPPR-CHtpDkWIgcuL_fUf935FF0auXdPdaTHBIyvEg3PUiMbaFyq-J8sHdHEvUvKwTPXwkXe0lRtLK3lkkgfSM_GSEGs1rnfqVqfUVZ_ThSAdIIIAWaqXhZlgs1JIWe7U2kdZU7jhVGKJxdHRB-PlD6e2IKqmQ1LF6N2As_IhZATPCs0FBjN0HHIi5rmtYcdh3ZAqJWDogNmJqVIOou1pIkNOv70yFUQUAFqrorXi4ahPCGIezifbK_tcosM8CqD5U1L4hdVK2yu0",
                "description": "Skincare, makeup, and hair care."
            },
            {
                "name": "Sports",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuAGWvbSrzqhzwIyn71eP8PArIx0Rl0crjfzDeH3R64UKCUrJIB5dkoqugGmHjAHWMsDIQApOe3EdBizCAVVfxBuPSfhMZUXI3wNye8WycNsxuyXA1hmKMqeUzmmr19WE8b-WythdVkRX65XgVYhrZSJG5bIAwI4lcgSqC2PDc1VKLtc0a-tTeVXXEek0mpVRj7En-Y8Bzbp_sfcLtyAPjYfN5D_B59yzb41O2Lsi-eRNfiQi61v3VJvSEd_9iV-Z4hi9i3ilmCOihA",
                "description": "Gym gear, athletic wear, and outdoor tools."
            },
            {
                "name": "Books",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDsHhLMK9iI6Kz3UaUzJ45uPINBMDaGoA7VG5d1hh_X3Ea_BOjlzKwQ1hC5q-wnnpZOSOoHngCi8bHa4gj-xj0JLg6fVWinmLtxqq5MfJ2DB6n_rxmsF1G-LL2JNfDOqxKc9J-n12TgWBWHJ4FMYSAORF1J6SF2E5uUb4gt63_eWVRX_NCBUQSXiBY4miPO8qdzZpkT_xRdbXL-vw_NF35WCMp336vqBEMdofzoJuipQXmJWQHO-j_Xm2tuDD3VjA2U8aO-DngUpC4",
                "description": "Fiction, non-fiction, and textbooks."
            },
            {
                "name": "Toys & Games",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuB3geG1SQNGGQOMUrwto1aCPJ70ITzUSU0_sO93qDMf9xYo2Lo9znuK6_fBKJxkukYln07W7bMiffhnqYKBOgY097mIjOofEnnebvrsJPpoajybUX2-e5baO1Cocajt3KidRlAatKJnoGVvMkj2CR2vUYDP_BIxZZ8yXq7TL0rDOLcpUQIyrPQ3bK5poa0Yt6l98-vNj49nISTQBvn5yMz4EUOtUEDNaJVAvvXF_iL1f9n-YNtv9_NNS16TVWJxgeatmaGqzJLyQMo",
                "description": "For kids and kids-at-heart."
            },
            {
                "name": "Accessories",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuC5_SPnou0bsaIWzub27094bfOD7bsboKHwr1Io5KsXIqFOZeQJZv11VMAKktVKzcY1bWb1uXx9w5owHv7ln6-nl9Pe3NxT-Pe3N8CChPmj-q5WSZg1OJ1CfWhG8-nKUEywkJpNIZdF6WIzCWXiKZ6M0RfoUed6Zz7jvnsNPQN7pm4qx15ZWL4XZrFuRb46HZHAS6QV8ZBZNeMyBTvldRO_MbMOh23XKBj-eLRvjp9Bk1nYNVwFyT6GC9E2YMfvKf-KZVwlNT4solU",
                "description": "Cases, watches, chargers, and premium lifestyle accessories."
            },
            {
                "name": "Computers",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuAfEbxpG-GD3z2eTflyKepfMdJGPKMlqig3S48_FHZfWepeNFxWPowH4CkP2AFJRQ21un8XR4aO2zPtpOnfPCAvYuf388NpH1DRLvHS9EEDNigcsIbr4h2x6g5OoFtTS--ssim7EqLSsM_oSsZuEEyrHUbfvjtn1o39tw7Nn6aJFw1JPSTyp5QuUkJNq6JnYhq5SmYsAycKoz3migTTlA_kLCx3Ia01YwMEV_xVmnJ5AgK14N_L6hdSOi6ArSAGk2yAnJEWVthnuLs",
                "description": "Desktop PCs, Laptops, and RAM."
            },
            {
                "name": "Grocery",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuC2o1qpchLbAPuUS-9Nf9CYtkYKisAx5Y-KvFSDCoBt9IzCOTAiKossI9xQ7VBEQBMtHVANICNMZlzBu48EXCtrmRqs-OMrvCkuHVvzVveipYjprxEsgyK-bZat8pvlLKmsgmy3wn5GNyV6KaPdN7O4XVP5kbYCEB7yNLQHKgbOEY_3yX4DJPZeQONanjkJ0IvFL-VPUt7ClAP9g52RFpS5WGtSIjBn7AFg5PjC1N8kFfkrm569nEZHP7dUoS7_zgbXAS1cRHps_Ls",
                "description": "Fresh produce and daily essentials."
            }
        ]

        categories_map = {}
        for cat_data in categories_data:
            slug = slugify(cat_data["name"])
            cat = Category.objects.create(
                slug=slug,
                name=cat_data["name"],
                image_url=cat_data["image_url"],
                description=cat_data["description"]
            )
            categories_map[slug] = cat
            self.stdout.write(f"Created category: {cat.name}")

        self.stdout.write("Seeding products...")
        products_data = [
            # 1. Electronics
            {
                "name": "Wireless Noise-Cancelling Headphones",
                "category_slug": "electronics",
                "price": 2499.00,
                "old_price": 4999.00,
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
                "description": "Experience premium audio clarity with these wireless over-ear noise-cancelling headphones. Featuring advanced ANC and 40H battery.",
                "rating": 4.5,
                "rating_count": 1240,
                "is_featured": True,
                "is_trending": True,
                "stock": 15,
                "specifications": {"Brand": "SoundMaster", "Battery": "40 Hours", "Weight": "250g", "Connectivity": "Bluetooth 5.3"}
            },
            {
                "name": "Smart Watch Series 7 Pro",
                "category_slug": "electronics",
                "price": 12999.00,
                "old_price": 15999.00,
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
                "description": "Minimalist designer smart watch with AMOLED touch screen, health tracking, and custom notification alerts.",
                "rating": 5.0,
                "rating_count": 850,
                "is_featured": True,
                "is_trending": True,
                "stock": 12,
                "specifications": {"Brand": "SphereWatch", "Battery": "7 Days", "Weight": "42g", "Display": "AMOLED"}
            },
            {
                "name": "Portable Bluetooth Speaker",
                "category_slug": "electronics",
                "price": 3499.00,
                "old_price": 5499.00,
                "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500",
                "description": "High fidelity fabric-wrapped portable Bluetooth speaker with strong bass and IPX7 water resistance.",
                "rating": 4.0,
                "rating_count": 320,
                "is_featured": True,
                "is_trending": False,
                "stock": 25,
                "specifications": {"Brand": "SphereBoom", "Battery": "20 Hours", "Water_Resistance": "IPX7"}
            },
            {
                "name": "4K Ultra HD Smart TV",
                "category_slug": "electronics",
                "price": 39999.00,
                "old_price": 49999.00,
                "image_url": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=500",
                "description": "Enjoy a cinematic home viewing experience with stunning 4K UHD picture quality and smart streaming built-in.",
                "rating": 4.6,
                "rating_count": 512,
                "is_featured": False,
                "is_trending": True,
                "stock": 8,
                "specifications": {"Brand": "SphereView", "Resolution": "3840x2160", "OS": "Android TV"}
            },
            {
                "name": "Wireless Charging Pad",
                "category_slug": "electronics",
                "price": 1499.00,
                "old_price": 2499.00,
                "image_url": "https://images.unsplash.com/photo-1622445262465-2481c4574875?w=500",
                "description": "Sleek and fast wireless charging pad compatible with all Qi-enabled devices. LED indicator keeps track of charge status.",
                "rating": 4.3,
                "rating_count": 180,
                "is_featured": False,
                "is_trending": False,
                "stock": 30,
                "specifications": {"Brand": "VoltPad", "Power": "15W", "Material": "Tempered Glass"}
            },

            # 2. Fashion
            {
                "name": "Premium Cotton Crewneck T-Shirt",
                "category_slug": "fashion",
                "price": 799.00,
                "old_price": 1299.00,
                "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
                "description": "Ultra-soft cotton blend crewneck t-shirt. Designed for ultimate everyday comfort and durability.",
                "rating": 4.4,
                "rating_count": 420,
                "is_featured": True,
                "is_trending": True,
                "stock": 100,
                "specifications": {"Material": "100% Organic Cotton", "Fit": "Regular Fit", "Color": "Classic Navy"}
            },
            {
                "name": "Slim Fit Denim Jeans",
                "category_slug": "fashion",
                "price": 1999.00,
                "old_price": 2999.00,
                "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
                "description": "Premium stretch denim jeans crafted with a modern slim fit and timeless indigo wash detail.",
                "rating": 4.5,
                "rating_count": 310,
                "is_featured": False,
                "is_trending": True,
                "stock": 60,
                "specifications": {"Material": "98% Cotton, 2% Elastane", "Fit": "Slim", "Pockets": "5"}
            },
            {
                "name": "Classic Leather Jacket",
                "category_slug": "fashion",
                "price": 4999.00,
                "old_price": 7999.00,
                "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500",
                "description": "Indulge in authentic style with this hand-finished premium dark leather jacket. Durable and stylish.",
                "rating": 4.8,
                "rating_count": 95,
                "is_featured": True,
                "is_trending": False,
                "stock": 15,
                "specifications": {"Material": "Genuine Leather", "Lining": "Polyester", "Color": "Black"}
            },
            {
                "name": "Breathable Running Sneakers",
                "category_slug": "fashion",
                "price": 2999.00,
                "old_price": 3999.00,
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500",
                "description": "Designed with a lightweight knit upper and high-performance cushion soles to power your strides.",
                "rating": 4.7,
                "rating_count": 520,
                "is_featured": False,
                "is_trending": True,
                "stock": 45,
                "specifications": {"Upper": "Knit Mesh", "Sole": "EVA Cushion", "Weight": "240g"}
            },
            {
                "name": "Wool Blend Winter Coat",
                "category_slug": "fashion",
                "price": 3999.00,
                "old_price": 5999.00,
                "image_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=500",
                "description": "Stay snug and sophisticated with this heavy-insulated double-breasted wool blend winter overcoat.",
                "rating": 4.6,
                "rating_count": 72,
                "is_featured": False,
                "is_trending": False,
                "stock": 20,
                "specifications": {"Material": "70% Wool, 30% Polyester", "Length": "Mid-length"}
            },

            # 3. Home & Kitchen
            {
                "name": "Multi-Functional Air Fryer",
                "category_slug": "home-kitchen",
                "price": 5999.00,
                "old_price": 8999.00,
                "image_url": "https://images.unsplash.com/photo-1621972750749-0fbb1abb7736?w=500",
                "description": "Crisp and healthy cooking with 360-degree rapid heat circulation. Easy digital controls and presets.",
                "rating": 4.7,
                "rating_count": 890,
                "is_featured": True,
                "is_trending": True,
                "stock": 20,
                "specifications": {"Capacity": "5.5 Liters", "Power": "1500W", "Presets": "8"}
            },
            {
                "name": "Stainless Steel Chef's Knife",
                "category_slug": "home-kitchen",
                "price": 1299.00,
                "old_price": 1999.00,
                "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500",
                "description": "Ultra-sharp professional culinary knife crafted with high-carbon German steel and ergonomic handle.",
                "rating": 4.5,
                "rating_count": 140,
                "is_featured": False,
                "is_trending": False,
                "stock": 40,
                "specifications": {"Blade": "High-carbon Steel", "Length": "8 inches"}
            },
            {
                "name": "French Press Coffee Maker",
                "category_slug": "home-kitchen",
                "price": 1499.00,
                "old_price": 2499.00,
                "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500",
                "description": "Brew rich and flavorful full-bodied coffee at home with double-wall heat-resistant borosilicate glass.",
                "rating": 4.4,
                "rating_count": 320,
                "is_featured": False,
                "is_trending": True,
                "stock": 50,
                "specifications": {"Capacity": "1 Liter", "Material": "Borosilicate Glass, Stainless Steel"}
            },
            {
                "name": "Ceramic Non-Stick Cookware Set",
                "category_slug": "home-kitchen",
                "price": 4999.00,
                "old_price": 6999.00,
                "image_url": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=500",
                "description": "Healthy non-toxic cooking set featuring high-grade aluminum base and durable PTFE-free non-stick coatings.",
                "rating": 4.6,
                "rating_count": 215,
                "is_featured": True,
                "is_trending": False,
                "stock": 15,
                "specifications": {"Pieces": "10-Piece Set", "Coating": "Ceramic Non-Stick"}
            },
            {
                "name": "Ergonomic Memory Foam Pillow",
                "category_slug": "home-kitchen",
                "price": 999.00,
                "old_price": 1499.00,
                "image_url": "https://images.unsplash.com/photo-1631679706909-1844bbd07221?w=500",
                "description": "Orthopedic contour pillow designed for superior neck alignment and soothing sleep comfort.",
                "rating": 4.2,
                "rating_count": 480,
                "is_featured": False,
                "is_trending": False,
                "stock": 60,
                "specifications": {"Fill": "Premium Memory Foam", "Cover": "Bamboo Fabric"}
            },

            # 4. Beauty
            {
                "name": "Hydrating Hyaluronic Acid Serum",
                "category_slug": "beauty",
                "price": 899.00,
                "old_price": 1499.00,
                "image_url": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500",
                "description": "Infused with pure HA and Vitamin B5, this daily skin treatment deeply hydrates and plumps up facial skin.",
                "rating": 4.6,
                "rating_count": 680,
                "is_featured": True,
                "is_trending": True,
                "stock": 80,
                "specifications": {"Volume": "30ml", "Skin_Type": "All Skin Types"}
            },
            {
                "name": "Organic Aloe Vera Gel",
                "category_slug": "beauty",
                "price": 349.00,
                "old_price": 499.00,
                "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500",
                "description": "100% pure cold-pressed aloe vera gel. Perfect for moisturizing skin, cooling sunburns, and hair conditioning.",
                "rating": 4.5,
                "rating_count": 1250,
                "is_featured": False,
                "is_trending": False,
                "stock": 150,
                "specifications": {"Purity": "99.8% Pure", "Organic": "Yes", "Volume": "200ml"}
            },
            {
                "name": "Matte Liquid Lipstick Set",
                "category_slug": "beauty",
                "price": 1199.00,
                "old_price": 1999.00,
                "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=500",
                "description": "Long-wearing velvet-smooth liquid lipstick set. High pigment shades that remain transfer-proof for 12 hours.",
                "rating": 4.3,
                "rating_count": 290,
                "is_featured": True,
                "is_trending": False,
                "stock": 35,
                "specifications": {"Shades": "6 Colors Set", "Finish": "Matte", "Wear": "12-Hours"}
            },
            {
                "name": "Vitamin C Brightening Face Cream",
                "category_slug": "beauty",
                "price": 599.00,
                "old_price": 899.00,
                "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500",
                "description": "Luminous facial moisturizer packed with antioxidant Vitamin C to target dark spots and uneven tone.",
                "rating": 4.4,
                "rating_count": 450,
                "is_featured": False,
                "is_trending": True,
                "stock": 90,
                "specifications": {"Volume": "50g", "Key_Ingredient": "Vitamin C, Kakadu Plum"}
            },
            {
                "name": "Herbal Nourishing Shampoo",
                "category_slug": "beauty",
                "price": 449.00,
                "old_price": 699.00,
                "image_url": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500",
                "description": "Gentle sulfate-free cleanser enriched with bhringraj, argan oil, and biotin to reduce hair fall and promote shine.",
                "rating": 4.2,
                "rating_count": 310,
                "is_featured": False,
                "is_trending": False,
                "stock": 110,
                "specifications": {"Volume": "300ml", "Sulfate_Free": "Yes"}
            },

            # 5. Sports
            {
                "name": "Non-Slip TPE Yoga Mat",
                "category_slug": "sports",
                "price": 1199.00,
                "old_price": 1999.00,
                "image_url": "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=500",
                "description": "Eco-friendly high-density TPE yoga mat. Offers dual-layer textured non-slip grips for workouts.",
                "rating": 4.6,
                "rating_count": 430,
                "is_featured": True,
                "is_trending": False,
                "stock": 70,
                "specifications": {"Material": "TPE Eco-friendly", "Thickness": "6mm", "Size": "183x61cm"}
            },
            {
                "name": "Adjustable Dumbbell Set 20kg",
                "category_slug": "sports",
                "price": 3999.00,
                "old_price": 5999.00,
                "image_url": "https://images.unsplash.com/photo-1638536532686-d610adfc8e5c?w=500",
                "description": "Sturdy cast iron weight plates with custom lock collars. Adapt your workout weights up to 20kg.",
                "rating": 4.8,
                "rating_count": 180,
                "is_featured": True,
                "is_trending": True,
                "stock": 25,
                "specifications": {"Weight": "20kg Total", "Material": "Chrome Steel, Cast Iron"}
            },
            {
                "name": "Stainless Steel Insulated Water Bottle",
                "category_slug": "sports",
                "price": 899.00,
                "old_price": 1299.00,
                "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500",
                "description": "Double-wall vacuum insulation keeps drinks cold for 24h or hot for 12h. Sturdy loop cap.",
                "rating": 4.5,
                "rating_count": 620,
                "is_featured": False,
                "is_trending": False,
                "stock": 85,
                "specifications": {"Capacity": "750ml", "Material": "18/8 Stainless Steel"}
            },
            {
                "name": "Professional Badminton Racket Set",
                "category_slug": "sports",
                "price": 1899.00,
                "old_price": 2999.00,
                "image_url": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=500",
                "description": "Carbon fiber rackets with ultra-high string tension. Comes with a storage bag and nylon shuttles.",
                "rating": 4.4,
                "rating_count": 120,
                "is_featured": False,
                "is_trending": True,
                "stock": 40,
                "specifications": {"Material": "Carbon Fiber", "Weight": "85g", "Tension": "24-26 lbs"}
            },
            {
                "name": "Sports Gym Duffle Bag",
                "category_slug": "sports",
                "price": 1299.00,
                "old_price": 1999.00,
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500",
                "description": "Durable water-resistant gym bag featuring dedicated wet pocket and ventilated shoe compartment.",
                "rating": 4.3,
                "rating_count": 340,
                "is_featured": False,
                "is_trending": False,
                "stock": 55,
                "specifications": {"Capacity": "35 Liters", "Material": "600D Water-resistant Polyester"}
            },

            # 6. Books
            {
                "name": "The Alchemist - Anniversary Edition",
                "category_slug": "books",
                "price": 299.00,
                "old_price": 399.00,
                "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
                "description": "Paulo Coelho's masterpiece about Santiago, an Andalusian shepherd boy who travels in search of worldly treasure.",
                "rating": 4.8,
                "rating_count": 5230,
                "is_featured": True,
                "is_trending": True,
                "stock": 200,
                "specifications": {"Author": "Paulo Coelho", "Format": "Paperback", "Language": "English"}
            },
            {
                "name": "Atomic Habits",
                "category_slug": "books",
                "price": 450.00,
                "old_price": 699.00,
                "image_url": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500",
                "description": "James Clear outlines a proven framework for improving every day, focusing on tiny changes that deliver massive results.",
                "rating": 4.9,
                "rating_count": 8940,
                "is_featured": True,
                "is_trending": True,
                "stock": 180,
                "specifications": {"Author": "James Clear", "Format": "Hardcover", "Pages": "320"}
            },
            {
                "name": "Sapiens: A Brief History of Humankind",
                "category_slug": "books",
                "price": 499.00,
                "old_price": 799.00,
                "image_url": "https://images.unsplash.com/photo-1618666012174-83b441c0bc76?w=500",
                "description": "Yuval Noah Harari explores the evolutionary history of humans, tracing the rise of Homo sapiens from ancient times.",
                "rating": 4.7,
                "rating_count": 4120,
                "is_featured": False,
                "is_trending": True,
                "stock": 90,
                "specifications": {"Author": "Yuval Noah Harari", "Format": "Paperback", "Pages": "512"}
            },
            {
                "name": "Thinking, Fast and Slow",
                "category_slug": "books",
                "price": 399.00,
                "old_price": 599.00,
                "image_url": "https://images.unsplash.com/photo-1592496431122-2349e0fbc666?w=500",
                "description": "Daniel Kahneman explains the two systems that drive our choices: fast, intuitive thinking, and slow, logical thinking.",
                "rating": 4.5,
                "rating_count": 1840,
                "is_featured": False,
                "is_trending": False,
                "stock": 60,
                "specifications": {"Author": "Daniel Kahneman", "Format": "Paperback", "Pages": "499"}
            },
            {
                "name": "Educated: A Memoir",
                "category_slug": "books",
                "price": 350.00,
                "old_price": 499.00,
                "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
                "description": "Tara Westover's unforgettable memoir of escaping a survivalist family in Idaho to pursue higher education.",
                "rating": 4.6,
                "rating_count": 2150,
                "is_featured": False,
                "is_trending": False,
                "stock": 75,
                "specifications": {"Author": "Tara Westover", "Format": "Paperback", "Pages": "352"}
            },

            # 7. Toys & Games
            {
                "name": "Wooden Educational Building Blocks",
                "category_slug": "toys-games",
                "price": 899.00,
                "old_price": 1499.00,
                "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=500",
                "description": "Crafted from natural beech wood with non-toxic paints. Develops toddler fine motor skills and spatial reasoning.",
                "rating": 4.7,
                "rating_count": 150,
                "is_featured": True,
                "is_trending": False,
                "stock": 40,
                "specifications": {"Material": "Beech Wood", "Blocks": "50 Pieces Set", "Age": "2+ Years"}
            },
            {
                "name": "Classic Monopoly Board Game",
                "category_slug": "toys-games",
                "price": 1199.00,
                "old_price": 1799.00,
                "image_url": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=500",
                "description": "The fast-dealing property trading game. Build houses and hotels, bankrupt your opponents, and win!",
                "rating": 4.5,
                "rating_count": 980,
                "is_featured": False,
                "is_trending": True,
                "stock": 100,
                "specifications": {"Players": "2-6 Players", "Age": "8+ Years"}
            },
            {
                "name": "Remote Control Off-Road Car",
                "category_slug": "toys-games",
                "price": 2499.00,
                "old_price": 3999.00,
                "image_url": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=500",
                "description": "1:16 scale all-terrain monster truck. Sturdy shock absorbers and 2.4GHz remote control for dual speed racing.",
                "rating": 4.6,
                "rating_count": 280,
                "is_featured": True,
                "is_trending": True,
                "stock": 30,
                "specifications": {"Speed": "20 km/h", "Battery": "Rechargeable Li-Po", "Scale": "1:16"}
            },
            {
                "name": "1000-Piece Nature Jigsaw Puzzle",
                "category_slug": "toys-games",
                "price": 699.00,
                "old_price": 999.00,
                "image_url": "https://images.unsplash.com/photo-1585241936939-be4099591252?w=500",
                "description": "High-quality recycled cardboard puzzle with a beautiful sunset landscape photo print. Anti-glare finish.",
                "rating": 4.4,
                "rating_count": 190,
                "is_featured": False,
                "is_trending": False,
                "stock": 65,
                "specifications": {"Pieces": "1000 Pcs", "Theme": "Scenic Nature"}
            },
            {
                "name": "Plush Soft Teddy Bear",
                "category_slug": "toys-games",
                "price": 499.00,
                "old_price": 799.00,
                "image_url": "https://images.unsplash.com/photo-1559251606-c623743a6d76?w=500",
                "description": "Soft and huggable brown teddy bear. Crafted with premium cotton fabrics and fluffy stuffing.",
                "rating": 4.7,
                "rating_count": 560,
                "is_featured": False,
                "is_trending": False,
                "stock": 120,
                "specifications": {"Size": "40 cm", "Material": "Plush Fabric"}
            },

            # 8. Accessories
            {
                "name": "Minimalist Silver Watch",
                "category_slug": "accessories",
                "price": 7500.00,
                "old_price": 9999.00,
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
                "description": "Minimalist designer wristwatch featuring white round dial, clean silver hands, and tan leather strap.",
                "rating": 4.2,
                "rating_count": 84,
                "is_featured": True,
                "is_trending": False,
                "stock": 20,
                "specifications": {"Brand": "Chrono", "Material": "Stainless Steel", "Strap": "Tan Leather"}
            },
            {
                "name": "Urban Aviator Sunglasses",
                "category_slug": "accessories",
                "price": 2800.00,
                "old_price": 3999.00,
                "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500",
                "description": "Sleek and classic dark aviators with robust silver metal frame, offering full UV400 protection.",
                "rating": 4.3,
                "rating_count": 52,
                "is_featured": True,
                "is_trending": False,
                "stock": 18,
                "specifications": {"Brand": "Urban Vision", "Frame": "Metal", "Protection": "UV400"}
            },
            {
                "name": "Premium Laptop Stand",
                "category_slug": "accessories",
                "price": 1299.00,
                "old_price": 1999.00,
                "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500",
                "description": "Ergonomic silver aluminum laptop stand designed for cooling, suitable for workspace efficiency.",
                "rating": 4.6,
                "rating_count": 140,
                "is_featured": False,
                "is_trending": False,
                "stock": 25,
                "specifications": {"Brand": "FlexiStand", "Material": "Aluminum", "Angle": "Adjustable"}
            },
            {
                "name": "Leather Bi-Fold Wallet",
                "category_slug": "accessories",
                "price": 1499.00,
                "old_price": 2499.00,
                "image_url": "https://images.unsplash.com/photo-1627124118304-4f4727931182?w=500",
                "description": "Handcrafted full-grain leather wallet with RFID blocking technology, 8 card slots, and currency pocket.",
                "rating": 4.5,
                "rating_count": 210,
                "is_featured": False,
                "is_trending": True,
                "stock": 45,
                "specifications": {"Material": "Full Grain Leather", "RFID_Blocking": "Yes"}
            },
            {
                "name": "Instant Film Camera",
                "category_slug": "accessories",
                "price": 5499.00,
                "old_price": 6999.00,
                "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500",
                "description": "Pastel blue instant film camera. Fun, creative, and prints memory snapshots immediately.",
                "rating": 4.1,
                "rating_count": 76,
                "is_featured": False,
                "is_trending": False,
                "stock": 15,
                "specifications": {"Brand": "InstantPix", "Color": "Pastel Blue", "Film": "Mini"}
            },

            # 9. Computers
            {
                "name": "Ultra-Slim 14-inch Laptop",
                "category_slug": "computers",
                "price": 45000.00,
                "old_price": 54999.00,
                "image_url": "https://images.unsplash.com/photo-1496181130204-7552cc1534e0?w=500",
                "description": "High performance computing in an ultra-portable profile. i5 Processor, 8GB RAM, and 512GB NVMe SSD.",
                "rating": 4.5,
                "rating_count": 180,
                "is_featured": True,
                "is_trending": True,
                "stock": 15,
                "specifications": {"Brand": "VoltBook", "Processor": "Intel Core i5", "RAM": "8GB", "Storage": "512GB SSD"}
            },
            {
                "name": "Mechanical Gaming Keyboard",
                "category_slug": "computers",
                "price": 3499.00,
                "old_price": 4999.00,
                "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500",
                "description": "Premium red switches with dynamic customizable RGB backlighting. Solid anodized aluminum top case.",
                "rating": 4.7,
                "rating_count": 340,
                "is_featured": True,
                "is_trending": False,
                "stock": 25,
                "specifications": {"Switches": "Mechanical Red", "Backlight": "RGB", "Layout": "Tenkeyless"}
            },
            {
                "name": "Wireless Ergonomic Mouse",
                "category_slug": "computers",
                "price": 1299.00,
                "old_price": 1999.00,
                "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500",
                "description": "Ergonomically sculpted layout reduces wrist fatigue. Multi-device Bluetooth and USB wireless receiver connection.",
                "rating": 4.4,
                "rating_count": 210,
                "is_featured": False,
                "is_trending": True,
                "stock": 60,
                "specifications": {"Brand": "LogiFit", "Battery": "Up to 120 Days", "DPI": "4000 Max"}
            },
            {
                "name": "Full HD 24-inch IPS Monitor",
                "category_slug": "computers",
                "price": 8999.00,
                "old_price": 11999.00,
                "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500",
                "description": "Three-sided borderless screen with rich IPS color gamut. AMD FreeSync and 75Hz refresh rate for seamless gameplay.",
                "rating": 4.6,
                "rating_count": 380,
                "is_featured": False,
                "is_trending": True,
                "stock": 18,
                "specifications": {"Display": "24 inch IPS", "Resolution": "1920x1080", "Refresh_Rate": "75Hz"}
            },
            {
                "name": "External 1TB Portable SSD",
                "category_slug": "computers",
                "price": 6499.00,
                "old_price": 9999.00,
                "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500",
                "description": "Pocket-sized solid state drive delivering blazing fast transfer rates up to 1050MB/s. Drop resistant.",
                "rating": 4.8,
                "rating_count": 420,
                "is_featured": False,
                "is_trending": False,
                "stock": 40,
                "specifications": {"Capacity": "1TB", "Interface": "USB 3.2 Gen 2", "Speed": "1050 MB/s"}
            },

            # 10. Grocery
            {
                "name": "Organic Roasted Almonds 500g",
                "category_slug": "grocery",
                "price": 599.00,
                "old_price": 899.00,
                "image_url": "https://images.unsplash.com/photo-1508061253366-f7da158b6d4b?w=500",
                "description": "Lightly salted oven-roasted almonds, rich in antioxidants, protein, and healthy dietary fats.",
                "rating": 4.5,
                "rating_count": 490,
                "is_featured": True,
                "is_trending": False,
                "stock": 100,
                "specifications": {"Organic": "Yes", "Roast": "Dry Roasted", "Weight": "500g"}
            },
            {
                "name": "Pure Natural Honey 500g",
                "category_slug": "grocery",
                "price": 299.00,
                "old_price": 450.00,
                "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=500",
                "description": "Raw unpasteurized forest flower honey. Sourced directly from local high-altitude apiaries.",
                "rating": 4.7,
                "rating_count": 810,
                "is_featured": False,
                "is_trending": True,
                "stock": 120,
                "specifications": {"Purity": "100% Raw", "Weight": "500g"}
            },
            {
                "name": "Premium Green Tea Bags 50ct",
                "category_slug": "grocery",
                "price": 349.00,
                "old_price": 499.00,
                "image_url": "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=500",
                "description": "Smooth and light green tea leaves handpicked from Himalayan tea fields. Pack of 50 bio-degradable bags.",
                "rating": 4.4,
                "rating_count": 230,
                "is_featured": False,
                "is_trending": False,
                "stock": 150,
                "specifications": {"Bags": "50 Bags", "Flavor": "Classic Jasmine Green"}
            },
            {
                "name": "Organic Extra Virgin Olive Oil 1L",
                "category_slug": "grocery",
                "price": 899.00,
                "old_price": 1299.00,
                "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500",
                "description": "First cold-pressed olives from Mediterranean groves. Superior flavor profiles for dressings and sautéing.",
                "rating": 4.8,
                "rating_count": 310,
                "is_featured": True,
                "is_trending": True,
                "stock": 80,
                "specifications": {"Volume": "1 Liter", "Acid_Level": "<0.8%"}
            },
            {
                "name": "Whole Grain Oats 1kg",
                "category_slug": "grocery",
                "price": 199.00,
                "old_price": 299.00,
                "image_url": "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=500",
                "description": "100% natural whole grain rolled oats. The perfect high-fiber nutrient-rich breakfast meal.",
                "rating": 4.5,
                "rating_count": 560,
                "is_featured": False,
                "is_trending": False,
                "stock": 200,
                "specifications": {"Weight": "1 kg", "Fiber": "10g per 100g"}
            }
        ]

        for prod_data in products_data:
            cat = categories_map.get(prod_data["category_slug"])
            if not cat:
                self.stdout.write(f"Category {prod_data['category_slug']} not found! Skipping product {prod_data['name']}")
                continue

            slug = slugify(prod_data["name"])
            # Generate unique slug in case of duplicate runs
            original_slug = slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            prod = Product.objects.create(
                slug=slug,
                name=prod_data["name"],
                category=cat,
                price=prod_data["price"],
                old_price=prod_data["old_price"],
                image_url=prod_data["image_url"],
                description=prod_data["description"],
                rating=prod_data["rating"],
                rating_count=prod_data["rating_count"],
                is_featured=prod_data["is_featured"],
                is_trending=prod_data["is_trending"],
                stock=prod_data["stock"],
                specifications=prod_data["specifications"]
            )
            self.stdout.write(f"Created product: {prod.name}")

        self.stdout.write("Database seeded successfully!")
