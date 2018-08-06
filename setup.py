import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wexapi",
    version="1.0.0-betta",
    license="MIT",
    author="Machin Dmytro",
    author_email="machin.dmitry+pypi.org@gmail.com",
    description="Wex.nz API Client (python)",
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
