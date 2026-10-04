from django.core.management.base import BaseCommand
from catalogue.models import Category, Product

class Command(BaseCommand):
    help = "Seeds demo categories and products into catalogue_db"

    def handle(self, *args, **options):
        self.stdout.write("Seeding categories and products...")

        # Categories
        cat_electronics, _ = Category.objects.get_or_create(
            slug="electronics",
            defaults={"name": "Electronics", "description": "Next-gen gadgets, audio, and smart tech"}
        )
        cat_apparel, _ = Category.objects.get_or_create(
            slug="apparel",
            defaults={"name": "Apparel", "description": "Premium streetwear and minimalist fashion"}
        )
        cat_lifestyle, _ = Category.objects.get_or_create(
            slug="lifestyle",
            defaults={"name": "Home & Lifestyle", "description": "Modern home essentials and workspace decor"}
        )

        demo_products = [
            {
                "name": "AeroSound Pro ANC Headphones",
                "slug": "aerosound-pro-anc-headphones",
                "sku": "AUD-HC-001",
                "category": cat_electronics,
                "price": "299.99",
                "stock": 15,
                "description": "High-fidelity wireless noise-canceling headphones with spatial audio, 40-hour battery, and memory foam earcups.",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80",
            },
            {
                "name": "UltraSlim M3 Mechanical Keyboard",
                "slug": "ultraslim-m3-mechanical-keyboard",
                "sku": "KBD-M3-002",
                "category": cat_electronics,
                "price": "149.50",
                "stock": 24,
                "description": "Low-profile RGB mechanical keyboard with hot-swappable tactile switches and anodized aluminum chassis.",
                "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&q=80",
            },
            {
                "name": "Horizon OLED Smartwatch Gen 4",
                "slug": "horizon-oled-smartwatch-gen-4",
                "sku": "WCH-GEN4-003",
                "category": cat_electronics,
                "price": "249.00",
                "stock": 8,
                "description": "Advanced health tracker with AMOLED display, ECG monitoring, GPS tracking, and titanium case.",
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80",
            },
            {
                "name": "Minimalist Leather Backpack",
                "slug": "minimalist-leather-backpack",
                "sku": "BAG-LTH-004",
                "category": cat_lifestyle,
                "price": "185.00",
                "stock": 12,
                "description": "Handcrafted full-grain leather laptop backpack with padded 16-inch compartment and weather resistance.",
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&q=80",
            },
            {
                "name": "Ergonomic Lumbar Desk Chair",
                "slug": "ergonomic-lumbar-desk-chair",
                "sku": "CHR-ERG-005",
                "category": cat_lifestyle,
                "price": "420.00",
                "stock": 5,
                "description": "Breathable mesh executive office chair with dynamic lumbar support, 4D armrests, and synchro-tilt mechanism.",
                "image_url": "https://images.unsplash.com/photo-1580481072645-022f9a6d8310?w=600&q=80",
            },
            {
                "name": "Urban Oversized Heavyweight Hoodie",
                "slug": "urban-oversized-heavyweight-hoodie",
                "sku": "APP-HD-006",
                "category": cat_apparel,
                "price": "79.99",
                "stock": 30,
                "description": "450 GSM organic French terry cotton hoodie with fleece lining and custom drop-shoulder fit.",
                "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600&q=80",
            },
            {
                "name": "SoundSphere 360 Portable Speaker",
                "slug": "soundsphere-360-portable-speaker",
                "sku": "AUD-SPK-007",
                "category": cat_electronics,
                "price": "119.00",
                "stock": 18,
                "description": "IPX7 waterproof Bluetooth speaker with 360-degree surround bass and 18-hour continuous playtime.",
                "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&q=80",
            },
            {
                "name": "Ceramic Matte Coffee Mug Set",
                "slug": "ceramic-matte-coffee-mug-set",
                "sku": "LFS-MUG-008",
                "category": cat_lifestyle,
                "price": "34.50",
                "stock": 40,
                "description": "Set of 4 artisan ceramic coffee mugs with heat-insulating silicone sleeves and minimalist matte finish.",
                "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80",
            },
        ]

        for p_data in demo_products:
            product, created = Product.objects.get_or_create(
                slug=p_data["slug"],
                defaults=p_data
            )
            if created:
                self.stdout.write(f"  Created product: {product.name}")
            else:
                self.stdout.write(f"  Product already exists: {product.name}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded catalogue demo data!"))
