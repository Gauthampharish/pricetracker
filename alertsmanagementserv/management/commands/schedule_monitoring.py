from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Schedule the monitoring task'

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )

        task_name = 'monitor_alerts_task'
        task, created = PeriodicTask.objects.get_or_create(
            name=task_name,
            defaults={
                'interval': schedule,
                'task': 'alertsmanagementserv.tasks.monitor_alerts',
            }
        )

        if not created:
            task.interval = schedule
            task.task = 'alertsmanagementserv.tasks.monitor_alerts'
            task.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully scheduled task: {task_name}'))