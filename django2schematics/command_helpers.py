from __future__ import absolute_import
from collections import defaultdict
import os
from django.core.exceptions import ImproperlyConfigured
from django.db.models.loading import get_app, get_models, get_model
from django2schematics.converter import SchematicsModel


def get_schematics_models(app_name):
    app = get_app(app_name)
    models =  get_models(app)
    all_models = []
    for model in models:
        all_models += SchematicsModel.from_django(model)
    return all_models


def get_models_to_output(*apps_or_models):
    """From a list of args, that can be either an app name or model name
    return a dict with app_name -> schematic models
    """
    app_model_dict = defaultdict(list)
    for item in apps_or_models:
        try:
            # if this is 'app_name.ModelName'
            app_name = '.'.join(item.split(".")[:-1])
            model_name = item.split('.')[-1]
            model = get_model(app_name, model_name)
            if not model:
                raise ImproperlyConfigured("")
            django_models = [model]
        except ImproperlyConfigured:
            # it's an app name
            django_models = get_models(get_app(item))
            app_name = item
        app_model_dict[app_name] += django_models
    return app_model_dict


def get_output(apps_or_models, to_file=False, auto_file_name='domain_auto', ):
    data = get_models_to_output(*apps_or_models)
    full_buffer = []
    for app_name, models in data.items():
        this_buffer = []
        these_models = []
        for model in models:
            these_models += SchematicsModel.from_django(model)
        this_buffer = [model.to_string() for model in these_models]
        if to_file:
            app_dir = os.path.dirname(models[0].__module__)
            output_file = os.path.join(app_dir, app_name, '%s.py' % auto_file_name)
            open(output_file, 'w').write("".join(this_buffer))
        full_buffer += this_buffer
    if not to_file:
        return "\n\n" + "\n\n\n".join(full_buffer)
