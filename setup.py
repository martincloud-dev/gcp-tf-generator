from setuptools import setup, find_packages
from terraform_gcp_generator import __version__

setup(
    name="terraform-gcp-generator",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "typer>=0.9.0",
        "pyyaml>=6.0.0",
        "jinja2>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "tf-gcp=terraform_gcp_generator.cli.app:main",
        ],
    },
    python_requires=">=3.8",
    author="YourName",
    author_email="your.email@example.com",
    description="Generador de proyectos Terraform para Google Cloud Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/terraform-gcp-generator",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 