import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'taxcalcindia'
copyright = '2026, Arumugam Maharaja'
author = 'Arumugam Maharaja'
release = '0.1.4'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',  # For better module summaries
]

# Autodoc settings to show ALL docstrings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',  # Show in source code order
    'special-members': '__init__',
    'undoc-members': True,
    'show-inheritance': True,
}

# Show type hints in description instead of signature
autodoc_typehints = 'description'

# Napoleon settings (for Google/NumPy docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = True

html_theme = 'sphinx_rtd_theme'
