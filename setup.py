from setuptools import find_packages, setup

with open("README.MD", "r") as f:
    long_description = f.read()

setup(
    name="snaptrade",
    version="1.1.0",
    description="A Python implementation of SnapTrade API client library",
    packages=find_packages(),
    package_data={"snaptrade": ["api_client/endpoints.json"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 7 - Inactive",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        "requests",
        "pycryptodome",
    ],
)
