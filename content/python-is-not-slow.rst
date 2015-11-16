#################################
Python is not necessarily slow
#################################

:date: 2015-11-15
:tags: Python, msprime, Newick trees
:category: Bioinformatics
:summary: Python can be very fast, if you get your layering right

I like Python. I think it's an ideal language for Bioinformatics, because
it allows us to make new things very quickly. There are first class
libraries for scientific computing like `numpy <http://www.numpy.org/>`_,
`scipy <http://www.scipy.org/>`_, `matplotlib <http://matplotlib.org/>`_,
`pandas <http://pandas.pydata.org/>`_ and many others that make us more
productive programmers. The `Python Package Index <https://pypi.python.org/pypi>`_
contains thousands of other packages to do all sorts of things, and we can
install and try out these packages in seconds using
`pip <https://docs.python.org/3/installing/>`_. The language itself is
very clean and easy to learn.

There is a persistent idea out there, however, that Python is too slow to
be of real use in large-scale Bioinformatics work. For example, if we
were to write a variant caller in Python, it would just be too slow. While
this is certainly true if we were to write *all* of the application in Python,
it's not *necessarily* true if we get our layering right.

One of the beauties of the design of Python is that we can easily incorporate
code written in C and C++ as `extension modules
<https://docs.python.org/3/extending/extending.html>`_. There are a variety of
ways of doing this. We can use the `Python C API
<https://docs.python.org/3/extending/index.html>`_ directly, or there are third
party tools such as `Cython <http://cython.org/>`_ to simplify the process.
This gives us the best of both worlds: the ease of programming and flexibility
of Python along with the speed of C and C++. However, people seem to
dismiss Python as still being somehow too inefficient.

I want to challenge this idea with an example using my coalescent simulator
`msprime <https://pypi.python.org/pypi/msprime>`_. The package provides a simple
`Python API <https://msprime.readthedocs.org/en/latest/api.html>`_ to allow
users run simulations and also analyse the resulting trees. The core of the
simulation and analysis code is written in C, but this is entirely hidden
from the user. Because we have a Python API to access the simulation code,
writing command line interface programs is really easy. The
`argparse <https://docs.python.org/3/library/argparse.html>`_ library lets
us write fully POSIX compliant CLIs in a very straightforward way, and
`setuptools <http://pythonhosted.org/setuptools/>`_ makes the proper
installation of these binaries incredibly easy.

Being able to write POSIX compliant command line interfaces that can be
installed into the user's system using standard methods is a big advantage over
C and C++ in my view. Writing CLIs in C is a huge pain. It's a surprisingly
time-consuming task because the standard `C library functions
<http://www.gnu.org/software/libc/manual/html_node/Getopt.html>`_ functions are
quite low-level. Inevitably, everyone has slightly different ideas for how a
command line interface should be structured, and so we have lots of 'quirky'
interfaces for bioinformatics programs. The Python `argparse
<https://docs.python.org/3/library/argparse.html>`_ module provides
standardised methods of handling subcommands, arguments, options, help output
and error handling. This means, for example, that I don't have to worry about
what the correct exit status is when the user provides bad input. I can get on
with writing interesting code that hasn't been done thousands of times before
by other people.

Correctly handling program installation is an even bigger gain, in my
opinion. While there are certainly good ways to handle the installation
of programs written in C and C++
(`autoconf <http://www.gnu.org/software/autoconf/autoconf.html>`_
and `cmake <https://cmake.org/>`_ for example), I don't think anyone
would argue that these are quick or easy. Installation must be done
via downloading a tarball, running :code:`./configure` and :code:`make install`. Using
Python, we can upload a package to PyPI and the user can then
install it with :code:`pip install <package-name>`.

We can use :code:`msprime` as an example. After installing the
`library dependencies <https://pypi.python.org/pypi/msprime>`_, we can
install the application using

.. code-block:: bash

    $ sudo pip install msprime

This installs two programs,
`msp <https://msprime.readthedocs.org/en/latest/cli.html#msp>`_
and
`mspms <https://msprime.readthedocs.org/en/latest/cli.html#mspms>`_,
into the appropriate location on the system (depending on the platform),
as well as installing the Python modules. We can then immediately
use the programs to run some simulations.

.. code-block:: bash

    $ msp simulate 1e5 out.hdf5 -m 1e8 -u 1e-3 -r 1e-3

Here we reproduce the simulation of 100,000 samples over a 100 megabase region
used by `Ryan Layer <https://twitter.com/ryanlayer>`_ and others to test out
their `GQT
<http://www.nature.com/nmeth/journal/vaop/ncurrent/full/nmeth.3654.html>`_
tool. The simulation took about 8 minutes and the output is a 102MB `HDF5
<https://www.hdfgroup.org/HDF5/>`_ file. This `HDF5 based format
<https://msprime.readthedocs.org/en/latest/file-format.html>`_ is only used by
:code:`msprime`, and so we provide some tools to convert to other widely used
formats. The command :code:`msp newick` takes a HDF5 tree sequence file as an
argument and writes out the encoded genealogies in `Newick format
<https://en.wikipedia.org/wiki/Newick_format>`_.

.. code-block:: bash

    $ /usr/bin/time -v msp newick out.hdf5 | head -n 10000 > subset.txt
    Command terminated by signal 13
    Command being timed: "msp newick out.hdf5"
    User time (seconds): 15.49
    System time (seconds): 5.44
    Percent of CPU this job got: 50%
    Elapsed (wall clock) time (h:mm:ss or m:ss): 0:41.40
    ...
    $ ls -lh subset.txt
    -rw-r--r-- 1 jk jk 19G Nov 15 16:46 subset.txt

In this example, we convert the the first 10,000 genealogies encoded in
:code:`out.hdf5` and write them to the file :code:`subset.txt`. This required a
user time of 15 seconds, and gave a 19G output file. Therefore, we output
Newick trees in this example at a rate of around 1.2 GB  per second, which it
is very unlikely the average I/O subsystem will be able to sustain for long.
There is therefore no real point in being faster than this, and if the entire
application was written in C from top-to-bottom, it's unlikely we would notice
any performance benefit.

Here is the current full implementation of the :code:`msp newick` command:

.. code-block:: python

    def run_dump_newick(args):
        tree_sequence = msprime.load(args.history_file)
        for length, newick in tree_sequence.newick_trees():
            print(newick)


While this is quite minimalistic, it serves to illustrate a couple of points:

1. Writing command line interfaces in Python is *easy*. Very little code
   will give you a fully functional, POSIX compliant program that is
   simple to deploy on a wide range of platforms.

2. Python programs do not need to be slow. They can write output as fast
   as you can reasonably expect any I/O system to consume it. If your
   application is layered appropriately, the difference in performance
   between a Python frontend and a full C application is negligible.


