from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'An Easy to use Open-Source Virtual Networking Framework for Python. Including Switches and Clients/Servers.'

# Setting up
setup(
    name="NewAlpha",
    version=VERSION,
    author="NewAlpha-VNet",
    author_email="<newalpha.help@gmx.net>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'iot', 'networking', 'socket', 'virtual-machine', 'server', 'switch', 'client', 'framework'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)