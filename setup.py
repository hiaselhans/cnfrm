import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cnfrm",
    version="0.0.1",
    author="hiaselhans",
    author_email="simon.klemenc@gmail.com",
    description="CnfRM - ORM for config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hiaselhans/CnfRM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)