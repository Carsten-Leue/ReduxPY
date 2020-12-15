# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'ReduxPy'
copyright = '2020, Dr. Carsten Leue'
author = 'Dr. Carsten Leue'

# The full version, including alpha/beta/rc tags
release = 'r1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosectionlabel',
    'sphinx_autodoc_typehints',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
    #    'autoapi.extension'
]

# Some config
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'rx': ('https://rxpy.readthedocs.io/en/latest/', None),
}
autosummary_generate = True
always_document_param_types = True
napoleon_use_ivar = True
autodoc_default_options = {
    'undoc-members': True
}

autoapi_type = 'python'
autoapi_dirs = ['../../redux']
autoapi_options = ['members', 'undoc-members',
                   'show-module-summary', 'imported-members']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
#html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
html_extra_path = ['.nojekyll']
