import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wexapi",
    version="0.1.0",
    author="Machin Dmitro",
    author_email="machin.dmitry+pypi.org@gmail.com",
    description="Wex.nz API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/madmis/wexapi",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
