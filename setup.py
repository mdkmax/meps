from setuptools import setup

setup(
    name='meps',
    packages=['meps'],
    include_package_data=True,
    install_requires=[
        'bs4',
        'flask',
        'requests',
        'validate_email',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
