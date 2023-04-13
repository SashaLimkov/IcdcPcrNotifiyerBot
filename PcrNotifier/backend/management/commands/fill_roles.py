from django.core.management import BaseCommand

# from backend.services.task_user import create_role
from backend.models import Role


class Command(BaseCommand):
    help = "Fill first batch to DB"

    def handle(self, *args, **options):
        Role.objects.create(name="Сотрудник")
        Role.objects.create(name="Глава отдела")
        Role.objects.create(name="Эпидемиолог")
        Role.objects.create(name="ЗГД")
