import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mygaz",
    version="0.0.1",
    author="Tom Elliott",
    author_email="tom.elliott@nyu.edu",
    description="Create, manage, and share ad hoc gazetteers",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: {pyver}",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['airtight', 'fuzzywuzzy[speedup]', 'pathvalidate', 'python-magic', 'python-slugify', 'requests', 'regex', 'textnorm'],
    python_requires='>=3.9.5'
)
