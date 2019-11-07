

from setuptools import setup, find_packages

dependencies = [x for x in open('./requirements.txt').read().strip().split('\n') if x.strip()]
test_dependencies = [x for x in open('./requirements-tests.txt').read().strip().split('\n') if x.strip()]

setup(
    name='skema',
    version=open('VERSION').read().strip(),

    description='Schema language that compiles to json schema',
    # long_description='',
    long_description_content_type='text/markdown',

    author='Tommaso De Rossi',
    author_email='daer.tommy@gmail.com',
    license='Apache Software License 2.0',

    url='https://github.com/remorses/schema',
    keywords=['schema', 'jsonschema', 'alternative', 'readable'],
    install_requires=dependencies,
    package_data={'': ['*.yaml', '*.json', '*.yml', 'VERSION']},
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        # 'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Information Technology',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=('tests',)),
    scripts=[
        'bin/skema',
    ],
    extras_require={
        'test': test_dependencies
    }

)


