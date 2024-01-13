import os
import re
from setuptools import setup, find_packages

required = []
with open('requirements.txt') as f:
    required = f.read().splitlines()

def docs_read(fname):
    return open(os.path.join(os.path.dirname(__file__), 'docs', fname)).read()

def version_read():
    settings_file = open(os.path.join(os.path.dirname(__file__),'protester','settings.py')).read()
    major_regex = """major_version\s*?=\s*?["']{1}(\d+)["']{1}"""
    minor_regex = """minor_version\s*?=\s*?["']{1}(\d+)["']{1}"""
    patch_regex = """patch_version\s*?=\s*?["']{1}(\d+)["']{1}"""
    major_match = re.search(major_regex, settings_file)
    minor_match = re.search(minor_regex, settings_file)
    patch_match = re.search(patch_regex, settings_file)
    major_version = major_match.group(1)
    minor_version = minor_match.group(1)
    patch_version = patch_match.group(1)
    if len(major_version) == 0:
        major_version = 0
    if len(minor_version) == 0:
        minor_version = 0
    if len(patch_version) == 0:
        patch_version = 0
    return major_version + "." + minor_version + "." + patch_version


setup(
    name='protester',
    version=version_read(),
    description='Testing Framework library for python',
    long_description=(docs_read('README.rst')),
    long_description_content_type="text/markdown",
    url='https://github.com/subramanya-a/ProTester',
    license='MIT license',
    author='Subramanya A',
    author_email='subramanya.opensource@gmail.com',
    platforms=['any'],
    packages=find_packages(include=["protester", "protester.*"]),
    # package_dir={'.': 'protester'},
    package_data={
        "protester": [
            # Include all report templates.
            "report/**/*",
        ],
    },
    entry_points={
        'console_scripts': [
            'protester = protester.__main__:main',
        ],
    },
    install_requires=required,
    keywords='Tester,protester,Automation,Testing Framework',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Topic :: Testing Framework :: Automation Testing',
        'Topic :: Tester',
        'Development Status :: 3 - Production/Stable',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
)