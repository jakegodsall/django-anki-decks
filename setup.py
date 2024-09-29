from setuptools import find_packages, setup

setup(
    name='djang-anki-decks',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A reusable Django app for extracting Anki decks from the .anki2 sqlite database file and managing '
                'them in a database table.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jakegodsall/django-anki-decks',
    author='Jake Godsall',
    author_email='jake.edward.godsall@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 5',
    ],
    install_requires=[
        'Django>=3.0',
    ],
)