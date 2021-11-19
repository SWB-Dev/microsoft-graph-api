import os

rootabspath = os.path.abspath(__file__)
rootdir = os.path.join(os.path.dirname(rootabspath))
ignores = ["__pycache__"]
packages = []


def traverse_package(paths:list):
    lookingdir = rootdir
    for p in paths:
        lookingdir = os.path.join(lookingdir,p)
    if os.path.isfile(lookingdir):
        return
    for dir in os.listdir(lookingdir):
        if dir not in ignores:
            next_path = paths.copy()
            next_path.append(dir)
            traverse_package(next_path)
    packages.append('.'.join(paths))

traverse_package(["msgraph"])

from setuptools import setup

setup(
    name="microsoft-graph-api",
    version="1.0.15",
    description="API for Microsoft Graph using refresh tokens.",
    url="https://github.com/SWB-Dev/microsoft-graph-api",
    author="Steven Barnes",
    author_email="steven.barnes@swbdevelopment.com",
    license="MIT",
    packages=packages,
    install_requires=["requests"])