from setuptools import setup, find_packages

setup(
    name="MEM_679_Minesweeper_JO_2",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'minesweeper=mem_679_minesweeper_jo_2.__main__:main',  # Points to main function
        ],
    },
    install_requires=[
        "pygame",  # Add any other dependencies here
    ],
)
