# docs/conf.py

import os
import sys

# -- Project information -----------------------------------------------------
project = 'cornerstone-community'
author = 'CORNERSTONE PDK team'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx_design',

]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "linkify",
    "substitution",
    "tasklist",
]


templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_book_theme'

html_theme_options = {
    "repository_url": "https://github.com/cornerstone-uos/cornerstone-community",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
}

master_doc = 'index'

html_static_path = ['_static']
html_css_files = ['custom.css']

source_suffix = {
    '.md': 'markdown',
}



