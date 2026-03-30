from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Min
from MyApp.models import teacher

class Command(BaseCommand):
    help = "This is some help text"

    def add_arguments(self, parser):
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--del', action='store_true')

    def handle(self, *args, **options):

        duplicate_field = 'Name'

        keep_ids = teacher.objects.values(duplicate_field).annotate(
            min_id=Min('id')
        ).values_list('min_id', flat=True)

        to_delete = teacher.objects.exclude(id__in=keep_ids)
        count = to_delete.count()

        if options['list']:
            if to_delete:
                for teach in to_delete:
                    print(teach.Name)
            else:
                print('No Duplicates Found')
        if options['del']:
            
            with transaction.atomic():
                to_delete.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} duplicate items.'))
