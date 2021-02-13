import setuptools
from distutils.core import setup

setup(
  name = 'didipack',
  packages = ['didipack'],
  version = '1.1.0',
  license='MIT',
  setup_requires=['wheel'],
  description = 'Usefull time saver for data-science and finance with python',
  author = 'Antoine Didisheim',
  author_email = 'antoinedidisheim@gmail.com',
  url = 'https://github.com/AntoineDidisheim',
  download_url = 'https://github.com/AntoineDidisheim/didipack/archive/v0.1.1.tar.gz',    # I explain this later on
  keywords = ['LaTex', 'Finance'],
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'statsmodels',
          'matplotlib'
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
)