from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from vegetables.models import Category, Vegetable
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho cửa hàng rau'

    def handle(self, *args, **options):
        # Tạo superuser nếu chưa có
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@rausach.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Đã tạo superuser: admin/admin123'))

        # Tạo danh mục
        categories_data = [
            {
                'name': 'Rau lá xanh',
                'description': 'Các loại rau lá tươi ngon, giàu vitamin và chất xơ'
            },
            {
                'name': 'Củ quả',
                'description': 'Củ và quả tươi ngon, bổ dưỡng'
            },
            {
                'name': 'Nấm',
                'description': 'Các loại nấm tươi, ngon và bổ dưỡng'
            },
            {
                'name': 'Gia vị',
                'description': 'Gia vị tự nhiên, tạo hương vị đặc trưng'
            },
            {
                'name': 'Rau thơm',
                'description': 'Các loại rau thơm tươi ngon'
            },
            {
                'name': 'Trái cây',
                'description': 'Trái cây tươi, ngon, giàu vitamin'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'Đã tạo danh mục: {cat.name}')

        # Tạo sản phẩm
        vegetables_data = [
            # Rau lá xanh
            {
                'name': 'Rau muống',
                'category': 'Rau lá xanh',
                'description': 'Rau muống tươi ngon, giàu vitamin A, C và sắt. Có thể chế biến nhiều món ngon.',
                'price': 25000,
                'unit': 'kg',
                'stock_quantity': 50,
                'is_featured': True,
                'nutritional_info': 'Giàu vitamin A, C, sắt, canxi. Tốt cho mắt và hệ tiêu hóa.',
                'origin': 'Đà Lạt'
            },
            {
                'name': 'Cải thìa',
                'category': 'Rau lá xanh',
                'description': 'Cải thìa baby tươi ngon, ngọt thanh, phù hợp cho nhiều món ăn.',
                'price': 30000,
                'unit': 'kg',
                'stock_quantity': 40,
                'is_featured': False,
                'nutritional_info': 'Chứa vitamin K, C, folate. Tốt cho xương và tim mạch.',
                'origin': 'Đà Lạt'
            },
            {
                'name': 'Rau dền',
                'category': 'Rau lá xanh',
                'description': 'Rau dền đỏ tươi ngon, giàu dinh dưỡng, tốt cho sức khỏe.',
                'price': 20000,
                'unit': 'kg',
                'stock_quantity': 35,
                'is_featured': False,
                'nutritional_info': 'Giàu sắt, protein thực vật, vitamin A.',
                'origin': 'Hà Nội'
            },
            # Củ quả
            {
                'name': 'Cà rốt',
                'category': 'Củ quả',
                'description': 'Cà rốt tươi ngon, giòn ngọt, giàu beta-carotene, tốt cho mắt.',
                'price': 35000,
                'unit': 'kg',
                'stock_quantity': 60,
                'is_featured': True,
                'nutritional_info': 'Giàu beta-carotene, vitamin A, chất xơ.',
                'origin': 'Đà Lạt'
            },
            {
                'name': 'Củ cải trắng',
                'category': 'Củ quả',
                'description': 'Củ cải trắng tươi ngon, giòn ngọt, thích hợp làm nhiều món.',
                'price': 22000,
                'unit': 'kg',
                'stock_quantity': 45,
                'is_featured': False,
                'nutritional_info': 'Chứa vitamin C, folate, chất xơ.',
                'origin': 'Đà Lạt'
            },
            {
                'name': 'Khoai tây',
                'category': 'Củ quả',
                'description': 'Khoai tây tươi ngon, bột, ngọt thanh, phù hợp chiên, luộc, nướng.',
                'price': 28000,
                'unit': 'kg',
                'stock_quantity': 80,
                'is_featured': True,
                'nutritional_info': 'Giàu tinh bột, vitamin C, kali.',
                'origin': 'Đà Lạt'
            },
            # Nấm
            {
                'name': 'Nấm kim châm',
                'category': 'Nấm',
                'description': 'Nấm kim châm tươi ngon, giòn, thích hợp cho lẩu và xào.',
                'price': 45000,
                'unit': 'kg',
                'stock_quantity': 25,
                'is_featured': False,
                'nutritional_info': 'Giàu protein, vitamin B, selenium.',
                'origin': 'Đà Lạt'
            },
            {
                'name': 'Nấm đùi gà',
                'category': 'Nấm',
                'description': 'Nấm đùi gà tươi ngon, thơm, giàu dinh dưỡng.',
                'price': 55000,
                'unit': 'kg',
                'stock_quantity': 20,
                'is_featured': True,
                'nutritional_info': 'Chứa protein cao, vitamin D, kali.',
                'origin': 'Đà Lạt'
            },
            # Gia vị
            {
                'name': 'Hành lá',
                'category': 'Gia vị',
                'description': 'Hành lá tươi ngon, thơm, thiết yếu trong bếp Việt.',
                'price': 15000,
                'unit': 'bundle',
                'stock_quantity': 30,
                'is_featured': False,
                'nutritional_info': 'Chứa allicin, vitamin C, chất chống oxy hóa.',
                'origin': 'Hà Nội'
            },
            {
                'name': 'Tỏi',
                'category': 'Gia vị',
                'description': 'Tỏi tươi ngon, thơm nồng, không thể thiếu trong nhà bếp.',
                'price': 40000,
                'unit': 'kg',
                'stock_quantity': 50,
                'is_featured': False,
                'nutritional_info': 'Giàu allicin, có tác dụng kháng khuẩn.',
                'origin': 'Lý Sơn'
            },
            # Rau thơm
            {
                'name': 'Rau húng quế',
                'category': 'Rau thơm',
                'description': 'Rau húng quế tươi ngon, thơm, ăn kèm với phở, bún.',
                'price': 20000,
                'unit': 'bundle',
                'stock_quantity': 25,
                'is_featured': False,
                'nutritional_info': 'Chứa tinh dầu, vitamin K, A.',
                'origin': 'Hà Nội'
            },
            {
                'name': 'Ngo gai',
                'category': 'Rau thơm',
                'description': 'Ngo gai tươi ngon, thơm đặc trưng, ăn kèm các món Việt.',
                'price': 25000,
                'unit': 'bundle',
                'stock_quantity': 20,
                'is_featured': False,
                'nutritional_info': 'Giàu vitamin C, K, chất xơ.',
                'origin': 'Hà Nội'
            },
            # Trái cây
            {
                'name': 'Cà chua',
                'category': 'Trái cây',
                'description': 'Cà chua chín đỏ, ngọt thanh, giàu lycopene.',
                'price': 32000,
                'unit': 'kg',
                'stock_quantity': 70,
                'is_featured': True,
                'nutritional_info': 'Giàu lycopene, vitamin C, kali.',
                'origin': 'Đà Lạt'
            },
            {
                'name': 'Dưa leo',
                'category': 'Trái cây',
                'description': 'Dưa leo tươi ngon, giòn mát, thích hợp ăn sống hoặc nộm.',
                'price': 18000,
                'unit': 'kg',
                'stock_quantity': 55,
                'is_featured': False,
                'nutritional_info': 'Chứa nhiều nước, vitamin K, C.',
                'origin': 'Đà Lạt'
            }
        ]

        for veg_data in vegetables_data:
            veg, created = Vegetable.objects.get_or_create(
                name=veg_data['name'],
                defaults={
                    'slug': slugify(veg_data['name']),
                    'category': categories[veg_data['category']],
                    'description': veg_data['description'],
                    'price': veg_data['price'],
                    'unit': veg_data['unit'],
                    'stock_quantity': veg_data['stock_quantity'],
                    'is_featured': veg_data['is_featured'],
                    'nutritional_info': veg_data['nutritional_info'],
                    'origin': veg_data['origin'],
                    'is_available': True
                }
            )
            if created:
                self.stdout.write(f'Đã tạo sản phẩm: {veg.name}')

        self.stdout.write(
            self.style.SUCCESS('Đã tạo xong dữ liệu mẫu!')
        )