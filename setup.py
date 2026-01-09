from setuptools import setup, find_packages

setup(
    name="taxcalcindia",
    version="0.1.3",
    author="Arumugam Maharaja",
    description="A package to calculate income tax for Indian taxpayers",
    author_email="raja1998civil@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
    ],
    keywords=["tax", "india tax", "income tax", "tax calculation", "itr", "tax assistance"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amrajacivil/taxcalcindia",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.9",
)