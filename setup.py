# Use the setuptools package if it is available. It's preferred 
# because it creates an exe file on Windows for Python scripts.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    

setup(name='aarhusinvwrapper',
      entry_points={'console_scripts': [ 
      #     'EXECUTABLE_NAME = package.subpackage.module:entry_function'
            ]
      })
