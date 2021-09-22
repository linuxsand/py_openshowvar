from setuptools import setup
import py_openshowvar

def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()
        
setup(
    name='py_openshowvar',
    version=py_openshowvar.__version__,
    description='A Python port of KUKA VarProxy client (OpenShowVar).',
    long_description=fread('README.rst'),
    url='https://github.com/linuxsand/py_openshowvar',
    author='Huang Jie',
    author_email='j.huang@reisrobotics.cn',
    license='MIT',
    py_modules=['py_openshowvar'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
