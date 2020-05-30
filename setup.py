from distutils.core import setup
setup(
  name = 'didipack',
  packages = ['didipack'],
  version = '0.1',
  license='MIT',
  description = 'Usfull time saver for data-science and finance with python',
  author = 'Antoine Didisheim',
  author_email = 'antoinedidisheim@gmail.com',
  url = 'https://github.com/AntoineDidisheim',
  download_url = 'https://github.com/AntoineDidisheim/didipack/archive/v01.tar.gz',    # I explain this later on
  keywords = ['LaTex', 'Finance'],
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'statsmodels'
      ],
  classifiers=[
    'Development Status :: MIT License',
    'Intended Audience :: Finance',      # Define that your audience are developers
    'Topic :: Data Science',
    'License :: OSI Approved :: Academic Free License v3.0',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)