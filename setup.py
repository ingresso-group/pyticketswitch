from distutils.core import setup

setup(
    name='IngressoXMLCoreInterface',
    version='1.0.0',
    author='Matt Jared',
    author_email='mattjared@ingresso.co.uk',
    packages=[
        'pyticketswitch',
        'pyticketswitch.test',
        'pyticketswitch.interface_objects'
    ],
    # url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='A Python interface for the Ingresso XML Core API',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
    ],
)
