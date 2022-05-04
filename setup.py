import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="adttools", # 
    version="1.0.1",
    author="kent010341",
    author_email="kent010341@gmail.com",
    description="Toolkit for calling Azure digital twins REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kent010341/azure-digital-twins-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords="adt, azure, digital twins",
    install_requires=["pandas"]
)
