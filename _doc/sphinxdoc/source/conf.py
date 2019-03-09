# -*- coding: utf-8 -*-
import sys
import os
import sphinxjp.themes.basicstrap
from pyquickhelper.helpgen.default_conf import set_sphinx_variables

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "manydataapi", "Xavier Dupré", 2019,
                     "basicstrap", None, locals(), add_extensions=None,
                     extlinks=dict(issue=('https://github.com/sdpython/manydataapi/issues/%s', 'issue')))

blog_root = "http://www.xavierdupre.fr/app/manydataapi/helpsphinx/"
blog_background = False

epkg_dictionary.update({
    "JCDecaux": 'http://www.jcdecaux.com/fr/pour-nos-partenaires/velos-en-libre-service',
    "linkedin": 'https://www.linkedin.com/',
    "LinkedIn": 'https://www.linkedin.com/',
    "velib": 'https://www.velib-metropole.fr/',
})
