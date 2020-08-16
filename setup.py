import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='ccsu-sp-f2020-poc-api',  
     version='1.0',
     scripts=['ccsu-sp-f2020-poc-api'] ,
     author="Anthony Brignano",
     author_email="anthony.brignano@gmail.com",
     description="CCSU - Senior Project - Fall 2020 - Proof of Concept - API",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/brignano/ccsu-sp-f2020-poc-api",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )