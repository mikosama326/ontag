from setuptools import setup

setup(
    name='Ontag',
    #version='1.0',
    py_modules=['ontag'],
    install_requires=[
        'Click',
        'tinydb',
        'tinytag',
        'colorama'
    ],
    entry_points="""
        [console_scripts]
        ontag=ontag:cli
    """
)
