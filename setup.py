
from setuptools import setup, find_packages

setup(
    name='lawu',
    packages=find_packages(),
    version='3.0.0',
    description='Doing fun stuff with JVM ClassFiles.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='Tyler Kennedy',
    author_email='tk@tkte.ch',
    url='http://github.com/TkTech/lawu',
    keywords=[
        'java',
        'disassembly',
        'disassembler',
        'assembly'
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Disassemblers'
    ],
    install_requires=[
        'click>=7.0'
    ],
    tests_require=[
        'pytest>=2.10',
        'pytest-cov'
    ],
    extras_require={
        'dev': [
            'pytest',
            'sphinx',
            'sphinxcontrib-googleanalytics',
            'sphinx_rtd_theme',
            'sphinx-click',
            'ghp-import',
            'pyyaml',
            'twine',
            'wheel'
        ]
    },
    entry_points='''
    [console_scripts]
    lawu=lawu.cli:cli
    '''
)
