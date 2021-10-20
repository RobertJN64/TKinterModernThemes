from setuptools import setup

setup(
    name='TKinterModernThemes',
    url='https://github.com/RobertJN64/TKinterModernThemes',
    author='Robert Nies',
    author_email='robertjnies@gamil.com',
    # Needed to actually package something
    packages=['TKinterModernThemes'],
    data_files=['README.md'], #because manifest is being stupid
    include_package_data=True,
    install_requires=[],
    extras_require={
        'matplotlib': ['matplotlib']
    },
    # *strongly* suggested for sharing
    version='1.6.0',
    # The license can be anything you like
    license='MIT',
    description='A collection of modern themes with code that makes it easy to integrate into a tkinter project..',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)