import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GoodParallel-maxv", # Replace with your own username
    version="0.0.1",
    author="Max Vilimpoc",
    author_email="goodparallel@vilimpoc.org",
    description="GoodParallel: A simple, parallel command-line runner using n processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nuket/GoodParallel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: System :: Shells",
        "Topic :: Utilities"
    ],
    python_requires='>=2.6',
)
