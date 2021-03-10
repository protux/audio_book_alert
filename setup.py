from setuptools import (
    find_packages,
    setup,
)

setup(
    name='Audio Book Alert',
    version='0.10',
    description='A script for getting alerted about new audio books on Audible via Telegram',
    author='protux',
    package_dir={'audio_book_alert': 'audio_book_alert'},
    packages=find_packages()
)
