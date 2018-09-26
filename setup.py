import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='krok',
    version='1.0.0',
    author='Dmitry Bashkatov',
    author_email='dbashkatov@gmail.com',
    description='Expose your local TCP server as Kubernetes service in remote cluster.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/smpio/krok',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    license='MIT',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'krok = krok.__main__:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
    ],
)
