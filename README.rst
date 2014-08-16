=================
Django2Schematics
=================

This module is a code generator, it can read Django models and outputs
corresponding ones for schematics.

Of course, this is code generation, therefore a damn bad idea. This won't
keep your stuff synced.

It's still useful, however. Sometimes you're converting a large Django code
base to domain models in schematics. In those cases, it's a royal pain to
mechanically retype hundreds of models and thousands of field definitions by
hand.
We have computers for that, you know.

You can either run this as a stand alone script or use it as a library.

As a Stand Alone Script
-----------------------
Add django2schematics to your `INSTALLED_APPS` settings. Then::

    python manage.py django2schematics app_name

You can specify full apps or models to export. By default the script will output
to stdout. The `--as-files` flag will save each app models into
`[app-dir]/domain-raw.py`.

See `--help` for more options.


As a Library
------------
If you'd rather process the ouput your self then::

    from django2scheamtics.exporter import SchematicsModel
    SchematicsModel.from_django(the_model_class)
    # or as a string
    SchematicsModel.from_django(the_model_class).to_string()


Feedback
--------
Let me know if this works (or doesn't) for you. Feedback is always welcome.

Feedback with accompanying pull requests and tests will buy you a beer on me next
time you're in São Paulo. Or tea, if that's your thing.


