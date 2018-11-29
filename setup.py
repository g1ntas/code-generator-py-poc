from setuptools import setup, find_packages

setup(
    name='accio',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    author='Gintas Ko',
    install_requires=[
        'GitPython',
        'chevron',
        'case-conversion'
    ],
    entry_points='''
        [console_scripts]
        accio=accio.cli:main
    '''
)
