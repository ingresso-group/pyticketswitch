from distutils.core import setup

setup(
    name='pyticketswitch',
    version='1.4.12',
    author='Matt Jared',
    author_email='mattjared@ingresso.co.uk',
    packages=[
        'pyticketswitch',
        'pyticketswitch.test',
        'pyticketswitch.interface_objects'
    ],
    license='LICENSE.txt',
    description='A Python interface for the Ingresso XML Core API',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
    ],
)
