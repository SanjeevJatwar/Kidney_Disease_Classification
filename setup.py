import setuptools
import os

# Read README if it exists, otherwise use default description
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "Kidney Disease Classification using Deep Learning"

version = "0.0.0"

Repo_name = "Kidney_Disease_Classification"
Author_name = "SanjeevJatwar"
src_repo = "cnnClassifier"
author_email = "jatwarsanjeev@gmail.com"

setuptools.setup(
    name= src_repo,
    version=version,
    author=Author_name,
    author_email=author_email,
    description="An end to end deep learning project,",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = f"https://github.com/{Author_name}/{Repo_name}",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"))