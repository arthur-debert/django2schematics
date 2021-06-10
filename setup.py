from distutils.core import setup

setup(
    name='Django2Schematics',
    version='0.1',
    packages=['django2schematics','django2schematics.test'],
    author='Arthur Debert',
    author_email='arthur@stimuli.com.br',
    license='LICENSE.txt',
    description='Generates shematics models from Django ones.',
    long_description=open('README.rst', 'r').read(),
    install_requires=[
        'django==2.2.24',
        'schematics==0.9-5',
        'nose==1.3.3'
    ]

)