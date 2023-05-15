from django.core.management.base import BaseCommand
from news.models import Category, Post


class Command(BaseCommand):
    help = 'Clean news from a category'

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Из какой категории Вы хотите удалить все новости?:\n_______')
        for category in Category.objects.all():
            self.stdout.write(f'{category.pk}: {category.new_category}')

        try:
            answer = int(input())
        except:
            raise ValueError('Вы ввели неверное число!')

        if 1 < answer < Category.objects.all().count():
            category = Category.objects.get(pk=answer)
            self.stdout.write(f'Вы действительно хотите удалить все новости из категории {category.new_category}?')
            answer = input().lower()
            if answer == 'yes' or answer == 'y':
                Post.objects.filter(categories=category).delete()
                self.stdout.write(self.style.SUCCESS('Все новости удалены успешно!'))
        else:
            self.stdout.write('Вы ввели число за пределами диапозона!')
