from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()


exec(open("errors/version.py", 'r').read())


setup(name="errors",
      version=__version__,
      description="User friendly errors",
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Documentation',
          'Topic :: Documentation :: Sphinx',
          'Topic :: Software Development:: Documentation'
      ],
      author="Alex Carney",
      author_email="alcarneyme@gmail.com",
      license='MIT',
      packages=['errors'],
      python_requires='>=3.0',
      entry_points={
          'console_scripts': [
              'errors.document = errors.document:main'
          ]
      },
      zip_safe=False)
