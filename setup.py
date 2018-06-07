from codecs import open as codecs_open
from setuptools import setup, find_packages


with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

# Parse the version from the pxmcli module.
with open('fio_area/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue


inst_reqs = [
    'click', 'cligj', 'Fiona', 'numpy', 'pyproj', 'Shapely'
]

setup(name='fio-area',
      version=version,
      description="Fiona CLI plugin to calculate areas",
      long_description=long_description,
      classifiers=[
          'Topic :: Scientific/Engineering :: GIS',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6'
      ],
      keywords='fiona',
      author=u"Damon Burgett",
      author_email='damon@mapbox.com',
      url='https://github.com/mapbox/fio-area',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=inst_reqs,
      extras_require={
          'test': ['pytest', 'pytest-cov'],
      },
      entry_points="""
      [fiona.fio_commands]
      area=fio_area.scripts.cli:area
      """)
