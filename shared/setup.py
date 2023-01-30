from setuptools import setup

setup(
    name="common",
    version="0.0.1",
    packages=["common"],
    install_requires=[
        "google-cloud-pubsub==2.14.0",
    ],
)
