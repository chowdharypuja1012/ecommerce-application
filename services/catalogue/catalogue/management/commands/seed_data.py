from django.core.management.base import BaseCommand
from catalogue.models import Category, Product

class Command(BaseCommand):
    help = "Seeds demo categories and products into catalogue_db"

    def handle(self, *args, **options):
        self.stdout.write("Seeding categories and products...")

        # Categories
        cat_sparkling, _ = Category.objects.get_or_create(
            slug="sparkling-juices",
            defaults={"name": "Sparkling Juices", "description": "Lightly carbonated real fruit superfruit sodas"}
        )
        cat_wellness, _ = Category.objects.get_or_create(
            slug="wellness-elixirs",
            defaults={"name": "Wellness Elixirs", "description": "Organic adaptogens, botanical teas, and citrus tonics"}
        )
        cat_lifestyle, _ = Category.objects.get_or_create(
            slug="lifestyle-merch",
            defaults={"name": "Lifestyle & Merch", "description": "Glassware, organic totes, and alldae. lifestyle gear"}
        )

        demo_products = [
            {
                "name": "Ginger Yuzu Superfruit Soda",
                "slug": "ginger-yuzu-superfruit-soda",
                "sku": "DRK-YZ-001",
                "category": cat_sparkling,
                "price": "249.00",
                "stock": 45,
                "description": "Lightly carbonated superfruit soda crafted with cold-pressed yuzu citrus, organic ginger root, and antioxidant extracts.",
                "image_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=700&q=80",
            },
            {
                "name": "Hibiscus Dragonfruit Elixir",
                "slug": "hibiscus-dragonfruit-elixir",
                "sku": "DRK-HB-002",
                "category": cat_sparkling,
                "price": "249.00",
                "stock": 50,
                "description": "Vibrant ruby sparkling elixir brewed with wild hibiscus flowers, pink dragonfruit puree, and electrolyte minerals.",
                "image_url": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=700&q=80",
            },
            {
                "name": "Passionfruit Guava Tropical Fizz",
                "slug": "passionfruit-guava-tropical-fizz",
                "sku": "DRK-PS-003",
                "category": cat_sparkling,
                "price": "249.00",
                "stock": 38,
                "description": "Sun-drenched passionfruit and pink guava sparkling juice with zero added artificial sugar or stevia.",
                "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=700&q=80",
            },
            {
                "name": "Matcha Citrus Carbonated Tonic",
                "slug": "matcha-citrus-carbonated-tonic",
                "sku": "DRK-MT-004",
                "category": cat_wellness,
                "price": "299.00",
                "stock": 30,
                "description": "Organic ceremonial Uji matcha blended with Meyer lemon juice and crisp sparkling spring water for clean focus.",
                "image_url": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=700&q=80",
            },
            {
                "name": "Blood Orange & Wild Berry Soda",
                "slug": "blood-orange-wild-berry-soda",
                "sku": "DRK-BO-005",
                "category": cat_sparkling,
                "price": "249.00",
                "stock": 60,
                "description": "Tart Sicilian blood orange juice paired with crushed raspberries and star anise botanicals.",
                "image_url": "https://images.unsplash.com/photo-1546171753-97d7676e4602?w=700&q=80",
            },
            {
                "name": "Ribbed Glassware Cold-Brew Tumbler",
                "slug": "ribbed-glassware-cold-brew-tumbler",
                "sku": "MRC-GL-006",
                "category": cat_lifestyle,
                "price": "1299.00",
                "stock": 20,
                "description": "Handcrafted ribbed borosilicate glass tumbler with glass straw and silicone spill-proof lid.",
                "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=700&q=80",
            },
            {
                "name": "Organic Cotton Citrus Shopper Tote",
                "slug": "organic-cotton-citrus-shopper-tote",
                "sku": "MRC-TT-007",
                "category": cat_lifestyle,
                "price": "899.00",
                "stock": 25,
                "description": "Heavyweight 100% organic unbleached cotton tote bag with signature alldae. fruit graphic print.",
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=700&q=80",
            },
            {
                "name": "Superfruit Variety Sampler (12 Cans)",
                "slug": "superfruit-variety-sampler-12-cans",
                "sku": "DRK-VR-008",
                "category": cat_sparkling,
                "price": "2699.00",
                "stock": 15,
                "description": "12-pack sampler featuring 3 cans each of Ginger Yuzu, Hibiscus Dragonfruit, Passionfruit Guava, and Matcha Citrus.",
                "image_url": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=700&q=80",
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

        self.stdout.write(self.style.SUCCESS("Successfully seeded alldae. demo products!"))
