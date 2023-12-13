import setuptools

setuptools.setup(
    name='didipack',
    packages=setuptools.find_packages(),  # Automatically discover and include all packages in the package directory
    version='4.3.21',
    license='MIT',
    setup_requires=['wheel'],
    description='Usefull time saver for data-science and finance with python',
    author='Antoine Didisheim',
    author_email='antoinedidisheim@gmail.com',
    url='https://github.com/AntoineDidisheim',
    download_url='https://github.com/AntoineDidisheim/didipack/archive/v0.1.1.tar.gz',
    keywords=['LaTex', 'Finance'],
    install_requires=[
        'numpy',
        'pandas',
        'statsmodels',
        'matplotlib',
        'jinja2',
        'tqdm',
        'scikit-learn'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    # If you have package data
    # package_data={
    #     'didipack': ['data/*.csv'],  # example, adjust as needed
    # },
)

