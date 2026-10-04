from django.core.management.base import BaseCommand
from catalogue.models import Category, Product

class Command(BaseCommand):
    help = "Seeds demo categories and products into catalogue_db"

    def handle(self, *args, **options):
        self.stdout.write("Seeding categories and products...")

        # Categories
        cat_cozy, _ = Category.objects.get_or_create(
            slug="cozy-living",
            defaults={"name": "Cozy Living", "description": "Handcrafted ceramics, ambient lighting, and aesthetic room decor"}
        )
        cat_tech, _ = Category.objects.get_or_create(
            slug="pastel-tech",
            defaults={"name": "Pastel Tech", "description": "Minimalist desk tech, mechanical keycaps, and plush audio gear"}
        )
        cat_apparel, _ = Category.objects.get_or_create(
            slug="aesthetic-apparel",
            defaults={"name": "Aesthetic Apparel", "description": "Soft streetwear, organic oversized hoodies, and woven totes"}
        )

        demo_products = [
            {
                "name": "Matcha Cloud Ceramic Mug",
                "slug": "matcha-cloud-ceramic-mug",
                "sku": "COZY-MUG-001",
                "category": cat_cozy,
                "price": "1499.00",
                "stock": 25,
                "description": "Artisan speckled stoneware ceramic mug with soft cream matte glaze and ergonomic thumb handle.",
                "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80",
            },
            {
                "name": "Pastel Dream Mechanical Keyboard",
                "slug": "pastel-dream-mechanical-keyboard",
                "sku": "TECH-KBD-002",
                "category": cat_tech,
                "price": "6999.00",
                "stock": 18,
                "description": "Wireless RGB mechanical keyboard featuring soft butter yellow and lavender keycaps with silent tactile switches.",
                "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&q=80",
            },
            {
                "name": "Lavender Cloud ANC Headphones",
                "slug": "lavender-cloud-anc-headphones",
                "sku": "TECH-AUD-003",
                "category": cat_tech,
                "price": "14999.00",
                "stock": 12,
                "description": "Ultra-plush wireless active noise-canceling headphones in dreamy soft lavender with memory foam cushions.",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80",
            },
            {
                "name": "Blush Pink Oversized Hoodie",
                "slug": "blush-pink-oversized-hoodie",
                "sku": "APP-HD-004",
                "category": cat_apparel,
                "price": "3499.00",
                "stock": 30,
                "description": "450 GSM organic French terry cotton hoodie with ultra-soft fleece lining in cozy blush pink.",
                "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600&q=80",
            },
            {
                "name": "Sage Botanical Scented Candle",
                "slug": "sage-botanical-scented-candle",
                "sku": "COZY-CND-005",
                "category": cat_cozy,
                "price": "1299.00",
                "stock": 40,
                "description": "Hand-poured coconut soy candle infused with wild sage, eucalyptus, and white cedar notes in an amber glass pot.",
                "image_url": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=600&q=80",
            },
            {
                "name": "Cream Canvas & Leather Tote",
                "slug": "cream-canvas-leather-tote",
                "sku": "APP-BAG-006",
                "category": cat_apparel,
                "price": "2899.00",
                "stock": 15,
                "description": "Minimalist heavy-duty organic canvas tote bag with full-grain leather straps and internal laptop sleeve.",
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&q=80",
            },
            {
                "name": "Butter Yellow Arch Desk Lamp",
                "slug": "butter-yellow-arch-desk-lamp",
                "sku": "COZY-LMP-007",
                "category": cat_cozy,
                "price": "4299.00",
                "stock": 10,
                "description": "Dimmable warm ambient LED arch lamp in matte butter yellow with integrated wireless phone charger base.",
                "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&q=80",
            },
            {
                "name": "Soft Sage Linen Weekly Journal",
                "slug": "soft-sage-linen-weekly-journal",
                "sku": "COZY-JRN-008",
                "category": cat_cozy,
                "price": "999.00",
                "stock": 50,
                "description": "Undated 52-week aesthetic goal journal bound in natural sage linen fabric with gold foil accents.",
                "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&q=80",
            },
        ]

        for p_data in demo_products:
            product, created = Product.objects.update_or_create(
                slug=p_data["slug"],
                defaults=p_data
            )
            if created:
                self.stdout.write(f"  Created product: {product.name}")
            else:
                self.stdout.write(f"  Updated product: {product.name} (price: INR {product.price})")

        self.stdout.write(self.style.SUCCESS("Successfully seeded Pinterest boutique demo data!"))
