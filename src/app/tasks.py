from datetime import timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone

from core.models import Todo

logger = get_task_logger(__name__)


@shared_task(bind=True)
def high_prioritized_todo_notification_task(self):
    """This task is scheduled to be launched minutely to notify those
    users that have got 'HIGH' priority tasks to be notified according
    to the set notification period at task moment
    """
    logger.info("The 'high_prioritized_todo_notification_task' "
                "celery task started.")

    def mock_send_email(send_todo: Todo) -> bool:
        """Mimic function to send email to the user."""
        if send_todo.user.email:
            logger.info("Email 'high_prioritized_todo_notification_task' sent "
                        "successfully to the user: %s",
                        send_todo.user.username)
        return True

    notification_alert_period = timezone.now() + timedelta(hours=3)
    todos_to_be_notified = Todo.objects.select_related('user').filter(
        priority=Todo.HIGH,
        is_notified=False,
        is_completed=False,
        to_be_notified=True,
        complete_before__lt=notification_alert_period,
    )
    # Low performant code below. Done in scope of technical challenge
    # to demonstrate of leveraging the celery for user being notified
    for todo in todos_to_be_notified:
        with transaction.atomic():
            try:
                if mock_send_email(todo):
                    todo.notified = True
                    todo.save()
            except Exception as err:
                logger.warning("Email 'high_prioritized_todo_notification_task' "
                               "failed to be sent to the user: %s. Error: %s",
                               todo.user.username, err)

    logger.info("The 'high_prioritized_todo_notification_task' "
                "celery task finished.")


@shared_task(bind=True)
def overdue_todo_notification_task(self):
    """This task is scheduled to be launched daily to notify those
    users that have got 'HIGH' priority tasks uncompleted and overdue.
    """
    logger.info("The 'overdue_todo_notification_task' celery task started.")

    def mock_send_email(send_todo: Todo) -> bool:
        """Mimic function to send email to the user."""
        if send_todo.user.email:
            logger.info("Email 'overdue_todo_notification_task' sent "
                        "successfully to the user: %s",
                        send_todo.user.username)
        return True

    overdue_todos_to_be_notified = Todo.objects.select_related('user').filter(
        priority=Todo.HIGH,
        is_notified=True,
        is_completed=False,
        complete_before__lt=timezone.now(),
    )
    # Low performant code below. Done in scope of technical challenge
    # to demonstrate of leveraging the celery for user being notified
    for todo in overdue_todos_to_be_notified:
        try:
            if mock_send_email(todo):
                todo.save()
        except Exception as err:
            logger.warning("Email 'overdue_todo_notification_task' "
                           "failed to be sent to the user: %s. Error: %s",
                           todo.user.username, err)

    logger.info("The 'high_prioritized_todo_notification_task' "
                "celery task finished.")
