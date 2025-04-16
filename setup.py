from setuptools import setup, find_packages

setup(
    name="fen_to_image",
    version="0.1.0",
    author="Théo Gueuret",
    author_email="tgueuret@live.fr",
    description="Convert fen as string to a PIL Image representing the position.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/to-grt/fen_to_image",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "pillow",
    ],
)
