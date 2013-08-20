from setuptools import setup
"""
This is the first application in Python
"""
setup(
    name="helloword",
    version="0.1.1",
    description="Print Hello word",
    author='Sara Czelusniak',
    author_email='arascz@gmail.com',
    classifiers=[
        "Programming Language :: Python",
        'Environment :: Console',
        ],
    license="free",
    packages=['helloword'],
    package_dir={'helloword': 'src/helloword'},
    test_suite='tests',
    )
