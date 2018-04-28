from setuptools import setup, find_packages


def readme():
    with open("README.rst") as f:
        return f.read()


exec(open("erratum/version.py", 'r').read())


setup(name="erratum",
      version=__version__,
      description="User friendly errors",
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Documentation',
          'Topic :: Documentation :: Sphinx',
          'Topic :: Software Development :: Documentation'
      ],
      author="Alex Carney",
      author_email="alcarneyme@gmail.com",
      license='MIT',
      packages=find_packages(exclude="tests"),
      python_requires='>=3.0',
      entry_points={
          'console_scripts': [
              'erratum.document = erratum.document:main'
          ]
      },
      tests_require = [
          'pytest',
          'pytest-cov',
          'hypothesis'
      ],
      setup_requires=['pytest-runner'],
      test_suite="tests",
      zip_safe=False)
