import setuptools
from os import path
root = path.curdir
with open(path.join(root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='richkit',
    description='Domain enrichment kit ',
    version='1.1.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aau-network-security/richkit',
    packages=setuptools.find_packages(exclude=['docs', 'richkit/test']),
    project_urls={
                'Bug Reports': 'https://github.com/aau-network-security/richkit/issues',
                'Funding': 'https://donate.pypi.org',
                'Source': 'https://github.com/aau-network-security/richkit',
    },
    install_requires=['maxminddb',
                      'numpy==1.17.2',
                      'scikit-learn==0.21.3',
                      'langid==1.1.6',
                      'bs4==0.0.1',
                      'lxml==4.6.3',
                      'requests==2.22.0',
                      'pytest',
                      'dnspython',
                      'coverage'],
    python_requires='>=3.5',
    author=['Ahmet Turkmen', 'Gian Marco Mennecozzi ', 'Egon Kidmose'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

)
