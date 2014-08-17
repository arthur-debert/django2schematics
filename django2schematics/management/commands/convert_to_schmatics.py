from django.core.management.base import LabelCommand
from django2schematics.command_helpers import get_output


class SchematicsOutputCommand(LabelCommand):
    args = '<app or model app_name or model ...>'
    label = 'label'

    def handle(self, *labels, **options):
        return get_output(
            to_file=options.get('to_file', False),
            auto_file_name=options.get('auto_file_name', None),
            *labels
        )
