from setuptools import setup, find_packages

setup(
    name="api-key-manager",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.0.0",
        "keyring>=23.0.0",
    ],
    entry_points={
        "console_scripts": [
            "api-key-manager=api_key_manager.main:main",
        ],
    },
    author="API Key Manager",
    description="A desktop application to securely store and manage API keys",
)
