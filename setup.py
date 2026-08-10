from setuptools import setup, find_packages

setup(
    name="empressiza-plant-matrix",
    version="1.0.0",
    author="The Plant Matrix",
    author_email="contact@theplantmatrix.com",
    description="Programmatic open-source botanical care database.",
    long_description="Open-source structured datasets tracking species-specific watering intervals and light requirements.",
    long_description_content_type="text/plain",
    url="https://theplantmatrix.com",
    project_urls={
        "Homepage": "https://theplantmatrix.com",
        "Source Code": "https://github.com",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
