from optparse import make_option
from django.core.management.base import BaseCommand
from django2schematics.command_helpers import get_output


class Command(BaseCommand):
    args = '<app or model app_name or model ...>'
    label = 'label'
    option_list = BaseCommand.option_list + (
        make_option('--to-file', action='store_true', dest='to_file', default=False,
            help="Save ouput into files on the app's directories"),
        make_option('--auto-file-name', action='store', dest='auto_file_name',
                    default='domain_auto',
            help='Which file name to store schematic models in'),
    )

    def handle(self, *labels, **options):
        return get_output(
            labels,
            to_file=options.get('to_file', False),
            auto_file_name=options.get('auto_file_name', None),
        )
