ydeos_weights
=============

.. image:: https://travis-ci.org/ydeos/ydeos_weights.svg?branch=main
    :target: https://travis-ci.org/ydeos/ydeos_weights

.. image:: https://app.codacy.com/project/badge/Grade/ecc23bca699645de87d8a5982b407243
    :target: https://www.codacy.com/gh/ydeos/ydeos_weights/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ydeos/ydeos_weights&amp;utm_campaign=Badge_Grade

.. image:: https://coveralls.io/repos/github/ydeos/ydeos_weights/badge.svg?branch=main
    :target: https://coveralls.io/github/ydeos/ydeos_weights?branch=main


**ydeos_weights** is a weights model library in Python 3.

A weight is approximated as a punctual mass present at a 3D point (Centre of Gravity of an object).

A weight can be added to a WeightsCollection. The WeightsCollection can be handled as a single Weight using its total weight
and the position of its centre of gravity.

Install
-------

**ydeos_weights** depends on:

- **PythonOCC** (OCC). See the PythonOCC_ repo for install instructions.
- **aocutils**. See the aoc-utils_ repo for install instructions.
- **ydeos_units**. See the ydeos_units_ repo for install instructions.

To install **ydeos_weights**:

.. code-block:: shell

   git clone https://github.com/ydeos/ydeos_weights
   cd ydeos_weights
   python setup.py install


.. _PythonOCC: https://github.com/tpaviot/pythonocc-core
.. _aoc-utils: https://github.com/guillaume-florent/aoc-utils
.. _ydeos_units: https://github.com/ydeos/ydeos_units


Examples
--------

See the examples_ folder.


.. _examples: https://github.com/ydeos/ydeos_weights/tree/main/examples


Contribute
----------

Please open an issue if you find a bug or if you come up with ideas about how to improve the project.

Then: fork, feature branch and open a pull request. Feel free to contribute!

