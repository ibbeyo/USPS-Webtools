from setuptools import setup, find_packages
import os

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as fs:
    long_description = fs.read()

setup(
    name='USPS-Webtools',
    version='0.0.1',
    description='Simple API for the USPS Webtools. No Authentication Required',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ibbeyo/USPS-Webtools',
    author='Ibbeyo',
    license='MIT',
    classifiers=classifiers,
    keywords=['usps', 'mail', 'package', 'tracking', 'zipcode'],
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.9.3',
        'bs4==0.0.1',
        'certifi==2022.12.7',
        'chardet==4.0.0',
        'fake-useragent==0.1.11',
        'idna==2.10',
        'requests==2.25.1',
        'soupsieve==2.2.1',
        'urllib3==1.26.4'
    ]
)