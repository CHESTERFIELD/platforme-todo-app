from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import User, Todo


class Command(BaseCommand):
    help = 'Adds test todo tasks and users'

    def handle(self, *args, **kwargs):
        # Create test users
        try:
            userone = User.objects.create_user(
                username='userone', email='userone@test.com', password='password')
            usertwo = User.objects.create_user(
                username='usertwo', email='usertwo@test.com', password='password')

            now = timezone.now()

            Todo.objects.create(user=userone, title='Test Todo 1',
                                priority=Todo.LOW, is_completed=True,
                                created_at=now - timedelta(days=1),
                                description='Very long description of very long '
                                            'test todo 1 for very long user one')

            Todo.objects.create(user=userone, title='Test Todo 2',
                                is_completed=False,
                                created_at=now - timedelta(hours=1),
                                description='Description of test todo 2')

            Todo.objects.create(user=userone, title='Test Todo 3',
                                priority=Todo.HIGH, is_completed=False,
                                to_be_notified=True,
                                complete_before=now + timedelta(hours=3,
                                                                minutes=3),
                                created_at=now - timedelta(hours=6),
                                description='Description of test todo 2')

            Todo.objects.create(user=userone, title='Test Todo 4',
                                priority=Todo.HIGH, is_completed=False,
                                to_be_notified=True, is_notified=True,
                                complete_before=now - timedelta(minutes=20),
                                created_at=now - timedelta(hours=1),
                                description='Description of test todo 4')

            Todo.objects.create(user=usertwo, title='Test Todo 1',
                                is_completed=False, priority=Todo.LOW,
                                created_at=now - timedelta(hours=1),
                                description='Description of test todo 1')

            Todo.objects.create(user=usertwo, title='Test Todo 2',
                                is_completed=False,
                                created_at=now - timedelta(hours=2),
                                description='Description of test todo 3')

            Todo.objects.create(user=usertwo, title='Test Todo 3',
                                is_completed=False, priority=Todo.HIGH,
                                created_at=now - timedelta(hours=3),
                                description='Description of test todo 3')
        except Exception as err:
            self.stdout.write(
                self.style.ERROR(f'Test data already exists. Error: {err}'))
            return

        self.stdout.write(self.style.SUCCESS('Test data added successfully.'))
