from setuptools import setup, find_packages
import glob

# Gather all .png files from the img directory
image_files = glob.glob('img/*.png')

setup(
    name="pokemath",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    data_files=[('img', image_files)],
    install_requires=[
       "beautifulsoup4==4.12.2",
       "pypokedex==1.6.0",
       "PyQt5==5.15.9",
       "requests==2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "pokemath = pokemath.__main__:main",
        ],
    },
)
