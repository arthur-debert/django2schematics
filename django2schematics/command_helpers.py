from __future__ import absolute_import
from collections import defaultdict
import os
from django.db.models.loading import get_app, get_models, get_model
from converter import SchematicsModel


def get_schematics_models(app_name):
    app = get_app(app_name)
    models =  get_models(app)
    return [SchematicsModel.from_django(model) for model in models]


def get_models_to_output(*apps_or_models):
    """From a list of args, that can be either an app name or model name
    return a dict with app_name -> schematic models
    """
    app_model_dict = defaultdict(list)
    for item in apps_or_models:
        try:
            # if this is 'app_name.ModelName'
            app_name = item.split(".")[:-1]
            model_name = item.split('.')[-1]
            model = get_model(app_name, model_name)
            django_models = [model]
        except:
            # it's an app name
            django_models = get_models(get_app(item))
            app_name = item
        app_model_dict[app_name] += [get_schematics_models(model) 
                           for model in django_models]
    return app_model_dict


def get_output(to_file=False, auto_file_name='domain_auto', *apps_or_models):
    data = get_models_to_output(*apps_or_models)
    full_buffer = []
    for app_name, models in data:
        if to_file:
            this_buffer = []
        else:
            this_buffer = full_buffer
        this_buffer.append("\n\n".join([model.to_string() for model in models]))
        if to_file:
            app_dir = os.path.dirname(models[0].__file__)
            output_file = os.path.join(app_dir, '%s.py' % auto_file_name)
            open(output_file, 'w').write(this_buffer)
    if not to_file:
        print "\n\n".join(full_buffer)
