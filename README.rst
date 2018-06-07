fio-area
========

.. image:: https://img.shields.io/pypi/v/fio-area.svg
   :target: https://circleci.com/gh/mapbox/fio-area

.. image:: https://circleci.com/gh/mapbox/fio-area.svg?style=svg
   :target: https://circleci.com/gh/mapbox/fio-area

.. image:: https://codecov.io/gh/mapbox/fio-area/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/mapbox/fio-area


.. code-block:: console

    Usage: fio area [OPTIONS] FEATURES...

    Options:
      -s, --summary               Output summary statistics only
      --calc-crs TEXT             Projection to calculate area in
                                  [DEFAULT=esri:54009]
      --sequence / --no-sequence  Write a LF-delimited sequence of texts
                                  containing individual objects or write a single
                                  JSON text containing a feature collection object
                                  (the default).
      --help                      Show this message and exit.


Installation
============

.. code-block:: console

    pip install fio-area
