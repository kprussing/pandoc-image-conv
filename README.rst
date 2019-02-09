Convert Pandoc Images to a Reasonable Format
============================================

When writing, it is important to have images.  These images can be in a
variety of formats including high resolution camera formats, hand
crafted SVG, output from plotting libraries, or other.  Unfortunately,
not all of these formats are supported by all output formats generated
by Pandoc_.  The default work around is to convert the images by hand
and then hand change all of the references in the Pandoc document.  But
what if you want to target multiple output formats?  Then you are stuck
with duplicates of the original image that you must track.

One step in the right direction is to use a tool like SCons_ to
automatically convert the images to the correct format.  This can be
accomplished with various Tools_.  But that leaves the wrong image names
in the ``Image`` elements of the Pandoc Abstract Syntax Tree (AST).
This filter addresses this problem by walking the AST and converting the
URL for each image into an appropriate format.  For example, LaTeX
outputs cannot directly load SVG, but the SVG can be converted to a PDF
which can be loaded.  The underlying assumption is that you want to use
a common image format based on the original source format.  When paired
with a ``Tool`` like scons-pandoc_ to handle the dependency resolution,
specifying how to generate multiple outputs from a common source becomes
easy.

.. _Pandoc: https://pandoc.org
.. _Tools: https://github.com/kprussing/scons-inkscape
.. _scons-pandoc: https://github.com/kprussing/scons-pandoc

Installation
------------

Run::

   python setup.py install

Alternatively, you can use ``develop`` or the ``--user`` flag if you
want to hack the filter or install for a single user.

Usage
-----

Simply write your Pandoc document as you normally would, except always
use the path to the original source image for ``Image`` elements.  Then
run Pandoc with the filter::

   pandoc --filter pandoc-image-conv.py example.md -t ... -o ...

In a LaTeX output, you will find all SVG images converted to a
``\subimport`` with the appropriate output from Inkscape.  Similarly,
you will find vector graphics converted to EMF in Word outputs.

.. note:: This filter changes the image path in the AST.  You must
          ensure the correct format file exists or Pandoc will fail to
          build stand alone outputs.

Limitations
-----------

This filter operates in an all or nothing fashion.  Meaning, all images
of a given format are converted to the same output format.  There is no
mechanism to to omit a subset of the images from the conversion process.
However, this is most likely what you want.  If the output document
format cannot support a specific image format, you need to convert all
of them.

The mapping of document formats and input image formats to output
formats is hard coded into the filter.  I do not have a clean way to
load this when the filter runs because some of the conversion are
non-trivial.  For example, SVG inputs for LaTeX output is changed to a
``RawInline`` to ``subimport`` a LaTeX file.  Thoughts on how to handle
user overrides are welcome.

