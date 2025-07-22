# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Authentication for user filing issue (must have read/write access to repository to add issue to)
USERNAME = 'YinChihHsiang'

# The repository to add this issue to
REPO_OWNER = 'YinChihHsiang'
REPO_NAME = 'ArXivDaily'

# Set new submission url of subject
NEW_SUB_URLS = [
    'https://arxiv.org/list/astro-ph/new',
    'https://arxiv.org/list/gr-qc/new',
    'https://arxiv.org/list/math-ph/new',
    'https://arxiv.org/list/hep-th/new'
]

# Keywords to search
KEYWORD_LIST = ["dark energy","black hole","modified gravity","general relativity","gravitational wave","shadow","light ring"]
# Keywords to exclude
KEYWORD_EX_LIST = ["AGN","active galactic nucleus"]
# Note that the 'Keywords' above are actually searched in the abstract instead of the real keyword section. 
