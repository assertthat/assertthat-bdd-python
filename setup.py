from distutils.core import setup
setup(
  name = 'assertthat-bdd',         # How you named your package folder (MyLib)
  packages = ['assertthat_bdd'],   # Chose the same as "name"
  version = '1.0.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python tools for integration with AssertThat BDD plugin for Jira',   # Give a short description about your library
  author = 'Nick Iles',                   # Type in your name
  author_email = 'support@assertthat.com',      # Type in your E-Mail
  url = 'https://github.com/assertthat/assertthat-bdd-python',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/assertthat/assertthat-bdd-python/archive/v1.0.0.tar.gz',
  keywords = ['assertthat', 'bdd', 'Jira', 'download features', 'upload features'],   # Keywords that define your package best
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers or testers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
