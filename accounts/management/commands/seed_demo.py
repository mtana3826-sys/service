from django.core.management.base import BaseCommand
from accounts.models import Branch, User

class Command(BaseCommand):
    help = "Создаёт демонстрационные точки и пользователей"

    def handle(self, *args, **options):
        branch_a, _ = Branch.objects.get_or_create(name="Точка А")
        branch_b, _ = Branch.objects.get_or_create(name="Точка Б")

        users = [
            ("+10000000001", "employee", branch_a),
            ("+10000000002", "manager", branch_a),
            ("+10000000003", "employee", branch_b),
            ("+10000000004", "manager", branch_b),
            ("+10000000005", "owner", None),
        ]

        for phone, role, branch in users:
            user, _ = User.objects.get_or_create(
                phone=phone,
                defaults={"role": role, "branch": branch},
            )
            user.role = role
            user.branch = branch
            user.is_active = True
            user.set_password("demo12345")
            user.save()

        self.stdout.write(self.style.SUCCESS(
            "Демонстрационные точки и пользователи созданы."
        ))