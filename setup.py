from setuptools import setup, find_packages

long_description = open("./package_additions/pypi_README.md", "r").read()

VERSION = '1.0.21'
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
    install_requires=['datetime'],
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