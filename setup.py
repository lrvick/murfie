from setuptools import setup

setup(
    name='murfie',
    version='0.1',
    author='Lance R. Vick',
    author_email='lance@lrvick.net',
    packages=['murfie'],
    scripts=['bin/murfie'],
    url='http://github.com/lrvick/murfie',
    license='LICENSE.md',
    description='''
    Murfie is a Python CLI tool and library for interacting with the
    undocumented murfie.com  API.
    ''',
    long_description=open('README.md').read(),
    package_data={
        '': [
            '../README.md',
            '../LICENSE.md',
            '../CHANGES.md',
            '../AUTHORS.md',
        ]
    },
    test_suite='tests',
    tests_require=[
        'flake8',
        'wheel',
        'tox',
        'mock',
    ],
    install_requires=[
        'setuptools',
        'BeautifulSoup4',
    ]
)
