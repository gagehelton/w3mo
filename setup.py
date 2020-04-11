from setuptools import setup

with open("./requirements.txt", "r")as f:
    req = f.read()
    f.close()

setup(name='w3mo',
        version='0.1.0',
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
        install_requires=req)
