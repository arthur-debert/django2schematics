from django.core.management.base import BaseCommand
from django2schematics.command_helpers import get_output


class Command(BaseCommand):
    args = '<app or model app_name or model ...>'
    label = 'label'

    def handle(self, *labels, **options):
        return get_output(
            labels,
            to_file=options.get('to_file', False),
            auto_file_name=options.get('auto_file_name', None),
        )
