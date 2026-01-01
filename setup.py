from setuptools import setup, find_packages

setup(
    name="taxcalcindia",
    version="0.1.0",
    author="Arumugam Maharaja",
    description="A package to calculate income tax for Indian taxpayers",
    author_email="raja1998civil@gmail.com",
    packages=find_packages(),
    install_requires=[
    ],
    keywords=["tax", "india", "income tax", "tax calculation"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amrajacivil/taxcalcindia"
)