
from setuptools import setup, find_packages

setup(
    name='jawa',
    packages=find_packages(),
    version='2.2.0',
    python_requires='>=3.6',
    description='Doing fun stuff with JVM ClassFiles.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='Tyler Kennedy',
    author_email='tk@tkte.ch',
    url='http://github.com/TkTech/Jawa',
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
        'Topic :: Software Development :: Disassemblers',
        'Topic :: Software Development :: Assemblers'
    ],
    install_requires=[
        'click>=5.0'
    ],
    tests_require=[
        'pytest>=2.10',
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
            'ipython',
            'twine',
            'wheel',
            'bumpversion'
        ]
    },
    entry_points='''
    [console_scripts]
    jawa=jawa.cli:cli
    '''
)
