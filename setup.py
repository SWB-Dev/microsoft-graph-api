from setuptools import setup

setup(
    name="microsoft-graph-api",
    version="0.3.2",
    description="API for Microsoft Graph using refresh tokens.",
    url="https://github.com/SWB-Dev/microsoft-graph-api/tree/develop",
    author="Steven Barnes",
    author_email="steven.barnes@swbdevelopment.com",
    license="MIT",
    packages=["msgraph","msgraph.graph","msgraph.sharepoint"],
    install_requires=["requests"])