import setuptools
import codecs, os, re

package = 'ttwidgets'

def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ttwidgets", 
    version=find_version(package, "__init__.py"),
    author="Gary Michael Bloom",
    author_email="bloominator@hotmail.com",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    data_files=[],
    description="Improved Tkinter widgets that accept HTML-like tagged text to support multiple fonts and enhanced visual schemes.",
    entry_points={},
    install_requires=[],
    license='Apache License 2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['ttwidgets', 'ttwidgets.test', ], # setuptools.find_packages(),
    package_data={},
    py_modules=[],
    python_requires='>=3.5',
    scripts=[],
    url="https://github.com/GaryBloom/ttwidgets",
)
