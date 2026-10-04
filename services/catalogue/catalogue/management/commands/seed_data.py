from django.core.management.base import BaseCommand
from catalogue.models import Category, Product

class Command(BaseCommand):
    help = "Seeds demo categories and products into catalogue_db"

    def handle(self, *args, **options):
        # Delete obsolete products and categories for clean catalog state
        Product.objects.all().delete()
        Category.objects.exclude(slug__in=[
            "stationery", "accessories", "home-decor", "gifts", "self-care", "flowers-and-wrapping"
        ]).delete()

        # Categories — cute lifestyle brand that matches the ruja aesthetic
        cat_stationery, _ = Category.objects.get_or_create(
            slug="stationery",
            defaults={"name": "Stationery", "description": "Beautiful journals, planners, washi tapes and pens"}
        )
        cat_accessories, _ = Category.objects.get_or_create(
            slug="accessories",
            defaults={"name": "Accessories", "description": "Hair clips, scrunchies, bows and cute little extras"}
        )
        cat_home_decor, _ = Category.objects.get_or_create(
            slug="home-decor",
            defaults={"name": "Home Decor", "description": "Candles, mugs, vases and cozy home accents"}
        )
        cat_gifts, _ = Category.objects.get_or_create(
            slug="gifts",
            defaults={"name": "Gifts", "description": "Curated gift boxes and hampers for every occasion"}
        )
        cat_self_care, _ = Category.objects.get_or_create(
            slug="self-care",
            defaults={"name": "Self Care", "description": "Bath bombs, face masks, essential oils and pampering treats"}
        )
        cat_flowers, _ = Category.objects.get_or_create(
            slug="flowers-and-wrapping",
            defaults={"name": "Flowers & Wrapping", "description": "Dried flowers, bouquets, gift wrap and ribbon"}
        )

        demo_products = [
            # ── Stationery ──
            {
                "name": "The Little Journal - Blush Pink",
                "slug": "the-little-journal-blush-pink",
                "sku": "STN-BJ-001",
                "category": cat_stationery,
                "price": "549.00",
                "stock": 40,
                "description": "A beautifully bound A5 lined journal in soft blush pink faux leather with gold foil lettering and ribbon bookmark.",
                "image_url": "/images/products/the-little-journal-blush-pink.jpg",
            },
            {
                "name": "Rose Gold Pen Set",
                "slug": "rose-gold-pen-set",
                "sku": "STN-RG-002",
                "category": cat_stationery,
                "price": "449.00",
                "stock": 50,
                "description": "Set of 3 sleek ballpoint pens with rose gold barrel and black ink. Comes in a pretty gift box.",
                "image_url": "/images/products/rose-gold-pen-set.jpg",
            },
            {
                "name": "Washi Tape Collection - Floral Dream",
                "slug": "washi-tape-floral-dream",
                "sku": "STN-WT-003",
                "category": cat_stationery,
                "price": "299.00",
                "stock": 60,
                "description": "Collection of 8 rolls of floral washi tape in pastel pink, lavender and sage patterns. Perfect for journaling.",
                "image_url": "/images/products/washi-tape-floral-dream.jpg",
            },
            {
                "name": "Gratitude Planner - 2026 Edition",
                "slug": "gratitude-planner-2026",
                "sku": "STN-GP-004",
                "category": cat_stationery,
                "price": "849.00",
                "stock": 30,
                "description": "Undated gratitude planner with monthly reflections, weekly spreads, habit tracker and affirmation pages. Hardcover, A5.",
                "image_url": "/images/products/gratitude-planner-2026.jpg",
            },

            # ── Accessories ──
            {
                "name": "Silk Satin Bow - Baby Pink",
                "slug": "silk-satin-bow-baby-pink",
                "sku": "ACC-SB-005",
                "category": cat_accessories,
                "price": "249.00",
                "stock": 70,
                "description": "Oversized silk satin bow hair clip in baby pink. Adds the cutest touch to any outfit. Alligator clip base.",
                "image_url": "/images/products/silk-satin-bow-baby-pink.jpg",
            },
            {
                "name": "Velvet Scrunchie Set - Pastels",
                "slug": "velvet-scrunchie-set-pastels",
                "sku": "ACC-VS-006",
                "category": cat_accessories,
                "price": "349.00",
                "stock": 55,
                "description": "Set of 5 premium velvet scrunchies in rose, lilac, sage, butter yellow and dusty blue. Super gentle on hair.",
                "image_url": "/images/products/velvet-scrunchie-set-pastels.jpg",
            },
            {
                "name": "Pearl Hair Clip Set - Gold",
                "slug": "pearl-hair-clip-set-gold",
                "sku": "ACC-PH-007",
                "category": cat_accessories,
                "price": "399.00",
                "stock": 45,
                "description": "Set of 4 faux-pearl hair clips in different shapes. Gold-plated pins, gentle grip, perfect for everyday wear.",
                "image_url": "/images/products/pearl-hair-clip-set-gold.jpg",
            },

            # ── Home Decor ──
            {
                "name": "Sunday Morning Mug - Lavender",
                "slug": "sunday-morning-mug-lavender",
                "sku": "HDC-MG-008",
                "category": cat_home_decor,
                "price": "699.00",
                "stock": 35,
                "description": "Handmade ceramic mug in dreamy lavender glaze. Microwave and dishwasher safe. Capacity: 350ml.",
                "image_url": "/images/products/sunday-morning-mug-lavender.jpg",
            },
            {
                "name": "Soy Wax Candle - Vanilla & Peony",
                "slug": "soy-wax-candle-vanilla-peony",
                "sku": "HDC-SC-009",
                "category": cat_home_decor,
                "price": "799.00",
                "stock": 30,
                "description": "Hand-poured soy wax candle with vanilla and peony fragrance. Burns for 40+ hours. Reusable ceramic jar.",
                "image_url": "/images/products/soy-wax-candle-vanilla-peony.jpg",
            },
            {
                "name": "Ceramic Trinket Dish - Blush",
                "slug": "ceramic-trinket-dish-blush",
                "sku": "HDC-TD-010",
                "category": cat_home_decor,
                "price": "499.00",
                "stock": 40,
                "description": "Adorable ceramic trinket dish with scalloped edge in blush pink. Perfect for rings, earrings and small treasures.",
                "image_url": "/images/products/ceramic-trinket-dish-blush.jpg",
            },

            # ── Gifts ──
            {
                "name": "Sweet Little Love - Gift Hamper",
                "slug": "sweet-little-love-gift-hamper",
                "sku": "GFT-SL-011",
                "category": cat_gifts,
                "price": "1999.00",
                "stock": 20,
                "description": "Curated gift box with a scented candle, bath salts, silk eye mask, dried flower posy and a handwritten card.",
                "image_url": "/images/products/sweet-little-love-gift-hamper.jpg",
            },
            {
                "name": "A Box of Joy - Birthday Hamper",
                "slug": "a-box-of-joy-birthday-hamper",
                "sku": "GFT-BJ-012",
                "category": cat_gifts,
                "price": "2499.00",
                "stock": 15,
                "description": "The ultimate birthday surprise box with fairy lights, photo frame, chocolates, confetti and a personalized note.",
                "image_url": "/images/products/a-box-of-joy-birthday-hamper.jpg",
            },
            {
                "name": "Thank You - Appreciation Box",
                "slug": "thank-you-appreciation-box",
                "sku": "GFT-TY-013",
                "category": cat_gifts,
                "price": "1499.00",
                "stock": 25,
                "description": "Say thank you with a kraft gift box filled with gourmet cookies, a mini succulent, a pretty pen and a gratitude card.",
                "image_url": "/images/products/thank-you-appreciation-box.jpg",
            },

            # ── Self Care ──
            {
                "name": "Rose Petal Bath Bomb Set",
                "slug": "rose-petal-bath-bomb-set",
                "sku": "SFC-RB-014",
                "category": cat_self_care,
                "price": "599.00",
                "stock": 40,
                "description": "Set of 4 handmade bath bombs infused with rose petals, essential oils and shea butter. Makes bath time dreamy.",
                "image_url": "/images/products/rose-petal-bath-bomb-set.jpg",
            },
            {
                "name": "Lavender Sleep Mist",
                "slug": "lavender-sleep-mist",
                "sku": "SFC-LS-015",
                "category": cat_self_care,
                "price": "449.00",
                "stock": 35,
                "description": "Calming pillow spray with organic lavender, chamomile and ylang ylang. Drift into the sweetest sleep.",
                "image_url": "/images/products/lavender-sleep-mist.jpg",
            },
            {
                "name": "Silk Eye Mask - Dusty Rose",
                "slug": "silk-eye-mask-dusty-rose",
                "sku": "SFC-EM-016",
                "category": cat_self_care,
                "price": "649.00",
                "stock": 30,
                "description": "Pure mulberry silk eye mask in dusty rose. Hypoallergenic, adjustable strap. Comes in a matching silk pouch.",
                "image_url": "/images/products/silk-eye-mask-dusty-rose.jpg",
            },

            # ── Flowers & Wrapping ──
            {
                "name": "Dried Flower Bouquet - Blush",
                "slug": "dried-flower-bouquet-blush",
                "sku": "FLW-DF-017",
                "category": cat_flowers,
                "price": "899.00",
                "stock": 25,
                "description": "Handpicked dried flower bouquet with roses, bunny tails and eucalyptus in soft blush and cream tones.",
                "image_url": "/images/products/dried-flower-bouquet-blush.jpg",
            },
            {
                "name": "Pastel Gift Wrapping Kit",
                "slug": "pastel-gift-wrapping-kit",
                "sku": "FLW-GW-018",
                "category": cat_flowers,
                "price": "399.00",
                "stock": 35,
                "description": "Complete wrapping kit with 4 pastel tissue papers, satin ribbon, dried flower sprig, gift tags and twine.",
                "image_url": "/images/products/pastel-gift-wrapping-kit.jpg",
            },
            {
                "name": "Mini Preserved Rose - Glass Dome",
                "slug": "mini-preserved-rose-glass-dome",
                "sku": "FLW-PR-019",
                "category": cat_flowers,
                "price": "1299.00",
                "stock": 15,
                "description": "Real preserved pink rose in an elegant glass dome with LED fairy lights. Lasts 2-3 years. No watering needed.",
                "image_url": "/images/products/mini-preserved-rose-glass-dome.jpg",
            },
            {
                "name": "Satin Ribbon Bundle - Blush & Cream",
                "slug": "satin-ribbon-bundle-blush-cream",
                "sku": "FLW-SR-020",
                "category": cat_flowers,
                "price": "199.00",
                "stock": 80,
                "description": "Bundle of 5 satin ribbons in blush pink, ivory, dusty rose, champagne and cream. 2 meters each. Perfect for gifts.",
                "image_url": "/images/products/satin-ribbon-bundle-blush-cream.jpg",
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

        self.stdout.write(self.style.SUCCESS("Successfully seeded ruja lifestyle products!"))
