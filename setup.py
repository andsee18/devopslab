from setuptools import setup, find_packages

setup(
    name="devops-lab5",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
    ],
    extras_require={
        "test": ["pytest", "httpx"],
    },
)