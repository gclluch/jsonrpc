from setuptools import setup, find_packages
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='jsonrpc-server-py',
    version='0.1',
    packages=find_packages(),
    description='A simple JSON-RPC server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gabriel Lluch',
    author_email='gclluch@gmail.com',
    license='MIT',
    url='https://github.com/gclluch/jsonrpc-server',
    project_urls={
        'Documentation': 'https://github.com/gclluch/jsonrpc-server/blob/main/README.md',
        'Source': 'https://github.com/gclluch/jsonrpc-server',
        'Tracker': 'https://github.com/gclluch/jsonrpc-server/issues',
    },
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'jsonrpc-server=jsonrpc_server:main',
        ],
    },
)

