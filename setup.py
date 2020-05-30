from distutils.core import setup
setup(
  name = 'didipack',
  packages = ['didipack'],
  version = '0.1',
  license='afl-3.0',
  description = 'Usfull time saver for data-science and finance with python',
  author = 'Antoine Didisheim',
  author_email = 'antoinedidisheim@gmail.com',
  url = 'https://github.com/AntoineDidisheim',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['LaTex', 'Finance'],
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Finance',      # Define that your audience are developers
    'Topic :: Data Science',
    'License :: OSI Approved :: Academic Free License v3.0',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)