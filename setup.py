import setuptools
import os.path

readme_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')

with open(readme_path, encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='ezvalue',
    version='0.1.1',
    description='An elegant and powerfull implementation of a value object.',
    long_description=long_description,
    
    url='https://github.com/snah/ezvalue',
    
    author='Hans Maree',
    author_email='hans.maree@gmail.com',
    
    license='MIT',
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    
    keywords='value valueobject immutable',
    
    packages=['ezvalue'],
    )
