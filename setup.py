from setuptools import setup, find_packages

setup(
    name='mazegen',
    version='1.0.0',
    description='A Maze Generator with three different algorithms',
    author="Laktaoui's team",
    author_email='abdalfattahlaktaoui98@gmail.com',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[],
    extras_require={
        'dev': [
            'mypy>=1.0.0',
            'pytest>=7.0.0',
            'flake8>=6.0.0',
        ],
    },
)
