"""
@author: Ross Drucker
"""
import setuptools

setuptools.setup(
    name='sportypy',
    version='0.0.9',
    url='https://github.com/rossdrucker/sportypy',
    author='Ross Drucker',
    author_email='ross.a.drucker@gmail.com',
    description='Facilitates drawing of regulation sports playing surfaces',
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
    ],
    zip_safe=False
)