from setuptools import setup, find_packages

setup(
    name="pokemath",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
       "beautifulsoup4==4.12.2",
       "pypokedex==1.6.0",
       "PyQt5==5.15.9",
       "requests==2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "pokemath = launcher:main",
        ],
    },
)
