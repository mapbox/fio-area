import os
from codecs import open as codecs_open
from setuptools import setup, find_packages


with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='fio-plugins',
    version='0.0.1',
    description="Fiona CLI plugin to calculate areas",
    long_description=long_description,
    classifiers=[],
    keywords='fiona',
    author=u"Damon Burgett",
    author_email='damon@mapbox.com',
    url='https://github.com/mapbox/fio-area',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=read('requirements.txt').splitlines(),
    extras_require={
        'test': ['pytest', 'pytest-cov', 'coveralls'],
    },
    entry_points="""
    [fiona.fio_commands]
    area=fio_area.scripts.cli:area
    """)
