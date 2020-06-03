from setuptools import setup

with open("./requirements.txt", "r")as f:
    req = f.read()
    f.close()

with open("./README.md","r")as f:
    long_description = f.read()

setup(name='w3mo',
        version=open("./version","r").read(),
        description='wemo control library',
        author='Gage Helton',
        author_email='gagehelton@gmail.com',
        url='https://github.com/mghelton/w3mo',
        packages=['w3mo'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=req)
