from setuptools import setup, find_packages

setup(
    name="saavn.py",
    version="0.1.0",
    author="0xhimangshu",
    author_email="saikiahimangshu@gmail.com",
    description="A Python client for the JioSaavn API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0xhimangshu/jiosaavn-main",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["aiohttp", "rich", "pynput"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    package_data={
        "saavn": ["__main__.py"],
    },
)
