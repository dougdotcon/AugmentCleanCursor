from setuptools import setup, find_packages

setup(
    name="augment-vip",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "tqdm>=4.62.0",
    ],
    entry_points={
        "console_scripts": [
            "augment-vip=augment_vip.cli:main",
        ],
    },
    python_requires=">=3.6",
    author="Augment VIP Team",
    description="Tools for managing VS Code settings for Augment VIP",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
