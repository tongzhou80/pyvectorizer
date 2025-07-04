from setuptools import setup, find_packages

setup(
    name="pyvectorizer",
    version="0.1.0",
    description="A tool to detect whether Python loops are vectorizable.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tong Zhou",
    author_email="zt9465@gmail.com",
    url="https://github.com/tongzhou80/pyvectorizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.7",
    install_requires=[],
    include_package_data=True,
)
