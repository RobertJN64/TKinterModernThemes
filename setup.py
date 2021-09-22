from setuptools import setup

def getPackages():
    out = []
    for item in ['azure', 'forest', 'park', 'sun-valley']:
        out.append('TKinterModernThemes/themes/' + item)
        out.append('TKinterModernThemes/themes/' + item + '/theme')
        out.append('TKinterModernThemes/themes/' + item + '/theme/dark')
        out.append('TKinterModernThemes/themes/' + item + '/theme/light')
    return out

setup(
    name='TKinterModernThemes',
    url='https://github.com/RobertJN64/TKinterModernThemes',
    author='Robert Nies',
    author_email='robertjnies@gamil.com',
    # Needed to actually package something
    packages=['TKinterModernThemes'],
    include_package_data=True,
    install_requires=[],
    # *strongly* suggested for sharing
    version='1.0.5',
    # The license can be anything you like
    license='MIT',
    description='A collection of modern themes with code that makes it easy to integrate into a tkinter project..',
    long_description=open('README.md').read(),
)