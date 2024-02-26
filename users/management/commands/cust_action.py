from django.core.management import BaseCommand
from users.models import User, Payment
from lms.models import Lesson, Course


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Удаление базы данных и наполнение данными """
        Payment.objects.all().delete()
        user1 = User.objects.get(pk=2)
        user2 = User.objects.get(pk=3)
        lesson1 = Lesson.objects.get(pk=1)
        lesson5 = Lesson.objects.get(pk=5)
        course2 = Course.objects.get(pk=2)

        # заполнение категорий
        payment_list = [{
            "pk": 1,
            "user": user1,
            "paid_lesson": lesson1,
            "payment_date": "2024-01-15",
            "amount": "100.00",
            "payment_type": 2,
        },
            {
                "pk": 2,
                "user": user1,
                "paid_lesson": lesson5,
                "payment_date": "2024-01-25",
                "amount": "107.00",
            },
            {
                "pk": 3,
                "user": user2,
                "paid_course": course2,
                "payment_date": "2024-01-25",
                "amount": "401.00",
            },
            {
                "pk": 4,
                "user": user1,
                "paid_course": course2,
                "payment_date": "2024-02-01",
                "amount": "421.00",
                "payment_type": 2,
            },
        ]
        # for item in category_list:
        #     Category.objects.create(**item)
        payments = []
        for payment in payment_list:
            payments.append(Payment(**payment))

        Payment.objects.bulk_create(payments)

        #
        # product_list = [{
        #     "pk": 1,
        #     "name": "морковь",
        #     "description": "морковь обыкновенная",
        #     "category": categories[0],
        #     "price": "30.99",
        # },
        #     {
        #         "pk": 2,
        #         "name": "капуста белокочанная",
        #         "description": "капуста обыкновенная",
        #         "category": categories[0],
        #         "price": "60.00",
        #     },
        #     {
        #         "pk": 3,
        #         "name": "яблоки",
        #         "description": "яблоко Леголь",
        #         "category": categories[1],
        #         "price": "70.50",
        #     },
        #     {
        #         "pk": 4,
        #         "name": "бананы",
        #         "description": "бананы Гондурас",
        #         "category": categories[1],
        #         "price": "121.99",
        #     },
        #     {
        #         "pk": 5,
        #         "name": "свинина",
        #         "description": "свинина экстра",
        #         "category": categories[2],
        #         "price": "379.99",
        #     },
        #     {
        #         "pk": 6,
        #         "name": "куриное филе",
        #         "description": "куриное филе Приосколье",
        #         "category": categories[2],
        #         "price": "254.50",
        #     },
        #     {
        #         "pk": 7,
        #         "name": "сок гранатовый",
        #         "description": "сок гранатовый первого отжима",
        #         "category": categories[3],
        #         "price": "229.99",
        #     },
        #     {
        #         "pk": 8,
        #         "name": "нектар манго",
        #         "description": "нектар манго осветленный",
        #         "category": categories[3],
        #         "price": "119.99",
        #     }, ]
        # products = []
        # for product in product_list:
        #     products.append(Product(**product))
        #
        # Product.objects.bulk_create(products)
