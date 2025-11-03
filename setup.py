"""
Setup script for pykumaapi2 package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pykumaapi2",
    version="0.1.1",
    author="Emad O. Medher",
    author_email="lsumedher@gmail.com",
    description="Python client for Uptime Kuma REST and Socket.io APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emadomedher/pyKumaAPI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    keywords="uptime-kuma monitoring api client socket.io rest pykumaapi2",
    project_urls={
        "Bug Reports": "https://github.com/emadomedher/pyKumaAPI/issues",
        "Source": "https://github.com/emadomedher/pyKumaAPI",
        "Documentation": "https://github.com/emadomedher/pyKumaAPI#readme",
    },
)
