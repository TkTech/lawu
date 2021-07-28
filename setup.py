
from setuptools import setup, find_packages

setup(
    name='lawu',
    packages=find_packages(),
    version='3.0.0',
    python_requires='>=3.7',
    description='Doing fun stuff with JVM ClassFiles.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='Tyler Kennedy',
    author_email='tk@tkte.ch',
    url='https://lawu.dev',
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
    tests_require=[
        'pytest>=2.10',
        'pytest-cov'
    ],
    install_requires=[
        'mutf8'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'sphinx',
            'sphinxcontrib-googleanalytics',
            'sphinx-click',
            'furo',
            'ghp-import',
            'pyyaml',
            'twine',
            'wheel'
        ],
        'cli': [
            'click',
            'rich'
        ]
    },
    entry_points='''
    [console_scripts]
    lawu=lawu.cli:cli
    '''
)
