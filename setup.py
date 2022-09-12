from setuptools import setup
from pathlib import Path


VERSION = '0.9'
DESCRIPTION = 'A cathode spot motion detection & analysis program'
LONG_DESCRIPTION = Path("README.md").read_text() 

# Setting up
setup(
    name= "blobber",
    version=VERSION,
    author="Jiongyu (Joey) Liang",
    author_email="joey.liang@sydney.edu.au",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    packages=['blobber'],
    install_requires=[
        'numpy',
        'matplotlib',
        'scikit-image',
        'Pillow',
        'joblib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
