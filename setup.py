from setuptools import setup, find_packages

with open("README.MD", "r") as f:
    long_description = f.read()

setup(
    name="snaptrade",
    version="0.0.1",
    description="A Python implementation of SnapTrade API client library",
    packages=find_packages(),
    package_data={"snaptrade":["api_client/endpoints.json"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)