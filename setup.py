# -*- coding: utf-8 -*-
import sys
import os
from setuptools import find_packages, setup
from pyquicksetup import read_version, read_readme, default_cmdclass


#########
# settings
#########

project_var_name = "manydataapi"
versionPython = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
path = "Lib/site-packages/" + project_var_name
readme = 'README.rst'
history = "HISTORY.rst"
requirements = None

KEYWORDS = [project_var_name, 'datasets', 'Xavier Dupré']
DESCRIPTION = """Pieces of code to access various API, most for teaching purposes."""
CLASSIFIERS = [
    'Programming Language :: Python :: %d' % sys.version_info[0],
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable'
]

#######
# data
#######

packages = find_packages('src', exclude='src')
package_dir = {k: "src/" + k.replace(".", "/") for k in packages}
package_data = {project_var_name + ".parsers.dummies": ["*.map"]}


setup(
    name=project_var_name,
    version=read_version(__file__, project_var_name, subfolder='src'),
    author='Xavier Dupré',
    author_email='xavier.dupre@gmail.com',
    license="MIT",
    url="http://www.xavierdupre.fr/app/manydataapi/helpsphinx/index.html",
    download_url="https://github.com/sdpython/manydataapi/",
    description=DESCRIPTION,
    long_description=read_readme(__file__),
    cmdclass=default_cmdclass(),
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    setup_requires=["pyquicksetup"],
    install_requires=["pyquickhelper"],
    extras_require={
        'velib.data_velib': ['moviepy'],
        'linkedin.linkedin_access': ['python3-linkedin'],
    },
)
