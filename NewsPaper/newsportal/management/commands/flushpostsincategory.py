from django.core.management.base import BaseCommand, CommandError
from newsportal.models import Post, Category


class Command(BaseCommand):
    help = "Enter Category to flush all posts in it."
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        category = Category.objects.get(category=options['category'])

        if category in Category.objects.all():
            self.stdout.write(f'Confirm deleting "{category.category}" posts')
            answer = input('Y/N: ').strip()
            if answer.lower() == 'y':
                amount = len(Post.objects.filter(category=category))
                Post.objects.filter(category=category).delete()
                self.stdout.write(
                    f'Successfully deleted {amount} "{category.category}" posts')
                return

        self.stdout.write(self.style.ERROR('Access denied'))
