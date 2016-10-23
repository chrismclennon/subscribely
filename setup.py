from setuptools import setup

setup(
    name='subscribely',
    packages=['subscribely'],
    include_package_data=True,
    install_requires=[
        'flask',
        'selenium',
        'pyjwt',
        'requests'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
