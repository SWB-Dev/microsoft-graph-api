from setuptools import setup

setup(
    name="microsoft-graph-api",
    version="1.0.3",
    description="API for Microsoft Graph using refresh tokens.",
    url="https://github.com/SWB-Dev/microsoft-graph-api",
    author="Steven Barnes",
    author_email="steven.barnes@swbdevelopment.com",
    license="MIT",
    packages=["msgraph","msgraph.graph","msgraph.graph.abstractions","msgraph.graph.implementations","msgraph.graph.utilities","msgraph.sharepoint","msgraph.sharepoint.abstractions","msgraph.sharepoint.implementations","msgraph.sharepoint.utilities"],
    install_requires=["requests"])