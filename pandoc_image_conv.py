#!/usr/bin/env python

import copy
import os

import panflute

def _Image_to_RawInline(img, ext):
    r"""Generate a LaTeX block from a :class:`panflute.Image`

    For LaTeX formats, we can have graphics in TikZ format or in the
    PDF=LaTeX format exported by Inkscape.  These need to use ``\input``
    instead of ``\includegraphics``.  Thus, we need to convert a
    :class:`panflute.Image` into a :class:`panflute.RawInline`.  For
    this, we take the root from the ``url`` and replace the extension
    with the provided extension.  The main text for the image is
    converted into LaTeX and used as the caption.
    """
    root, _ = os.path.splitext(img.url)
    dirname, root = os.path.split(root)
    dirname = os.path.join(dirname if dirname else os.curdir, "")

    caption = panflute.convert_text(panflute.Para(*img.content),
                                    "panflute", "latex")
    text = "\\begin{figure}\n" \
        + ( "\\hypertarget{{{0}}}{{%\n".format(img.identifier) \
            if img.identifier else "" ) \
        + "\\centering\n" \
        + "\\subimport{{{0}}}{{{1}}}\n".format(dirname, root + ext) \
        + "\\caption{{{0}}}".format(caption) \
        + ( "\\label{{{0}}}\n}}".format(img.identifier) \
            if img.identifier else "" ) \
        + "\n\\end{figure}"
    return panflute.RawInline(text, format="latex")

def _extension_swap(img, ext):
    """Convert the ``url`` extension of an image to that given
    """
    root, _ = os.path.splitext(img.url)
    img.url = root + ext
    return img


# Replacing an :class:`panflute.Image` is a simple matter of considering
# the input :class:`panflute.Image` type and the target
# :class:`panflute.Doc`.  A given combination simply needs to update the
# extension, generate the appropriate type like a
# :class:`panflute.RawInlne`, or simply do nothing.  This looks like a
# job for ``lambda`` functions!  To figure out what to do, we define a
# dictionary of dictionaries.  The top level keys are the target
# formats.  The secondary keys are the input extensions while the values
# are the callable to do the conversion.  The callable must take a
# single argument of :class:`panflute.Image` and return an
# :class:`panflute.Inline` or :class:`panflute.Image`.  This procedure
# assumes that the means to do the actual image conversion are defined
# in some way so that the final document can be produced.  If the target
# format and input extension are not included, nothing will be done to
# the image.
_extmap = {
        "docx" : {
                ".eps"  : lambda x: _extension_swap(x, ".emf"),
                ".png"  : lambda x: x,
                ".pdf"  : lambda x: _extension_swap(x, ".emf"),
                ".pgf"  : lambda x: _extension_swap(x, ".emf"),
                ".svg"  : lambda x: _extension_swap(x, ".emf"),
                ".tex"  : lambda x: _extension_swap(x, ".emf"),
                ".tikz" : lambda x: _extension_swap(x, ".emf"),
            },
        "html" : {
                ".eps"  : lambda x: _extension_swap(x, ".pdf"),
                ".png"  : lambda x: x,
                ".pdf"  : lambda x: x,
                ".pgf"  : lambda x: _extension_swap(x, ".svg"),
                ".svg"  : lambda x: x,
                ".tex"  : lambda x: _extension_swap(x, ".svg"),
                ".tikz" : lambda x: _extension_swap(x, ".svg"),
            },
        "latex" : {
                ".eps"  : lambda x: _extension_swap(x, ".pdf"),
                ".png"  : lambda x: x,
                ".pdf"  : lambda x: x,
                ".pgf"  : lambda x: _Image_to_RawInline(x, ".pgf"),
                ".svg"  : lambda x: _Image_to_RawInline(x, ".pdf_tex"),
                ".tex"  : lambda x: _Image_to_RawInline(x, ".tex"),
                ".tikz" : lambda x: _Image_to_RawInline(x, ".tikz"),
            },
    }


# Quite a few formats are extensions to, specifications of, or simply
# similar enough to  those defined above that we can just use the same
# mapping.  In that case, we don't want to rewrite the mappings.
# Instead, we'll simply map those extensions back to the appropriate
# case.  To do that, we use a dictionary whose keys are the predefined
# formats and the values are tuples of the new formats.
_additional = {
        "html" : (
            "html5",
            "slideous",
            "slidy",
            "dzslides",
            "revealjs",
            "s5",
        ),
        "latex" : (
            "beamer",
        ),
        "docx" : (
            "odt",
            "opendocument",
            "pptx",
        ),
    }
for src in _additional:
    for tgt in _additional[src]:
        _extmap[tgt] = _extmap[src]

# Duplicate the docx conversion and replace the GIF.  We want to use GIF
# in Powerpoint but not Word.  Similarly, we want to replace GIFs in
# LaTeX with PNG.
_extmap["docx"] = copy.deepcopy(_extmap["docx"])
for f in ("docx", "latex"):
    _extmap[f][".gif"] = lambda x: _extension_swap(x, ".png")

def _filter(elem, doc):
    """Select the conversion using the extension map

    If the format/extension pair is in the mapping dictionary, we run
    the function.  Otherwise, we just do nothing.
    """
    if type(elem) == panflute.Image and doc.format in _extmap:
        _, ext = os.path.splitext(elem.url)
        if ext in _extmap[doc.format]:
            elem = _extmap[doc.format][ext](elem)
            # panflute.debug("{0}".format(elem))
            return elem


def main(doc=None):
    return panflute.run_filter(_filter, doc)


if __name__ == "__main__":
    main()

