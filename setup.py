"""
coding: utf-8
@Software: PyCharm
@Time:  7:48
@Author: Fake77
@Module Name:
"""
import setuptools

with open("README.MD", 'r', encoding='utf-8') as des:
    long_description = des.read()


setuptools.setup(
    name='TB4hooky',
    version='0.1.5',
    author='Fake77',
    author_email="yankail520@gmail.com",
    description='Python hook framework support Local hook and Remote hook',
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8;",
    url='https://github.com/fateofdate/TB4hooky',
    include_package_data=False,
    install_requires=[
        "requests==2.31.0",
        "urllib3==1.26.6",
        "loguru==0.7.2",
        "win32-setctime==1.1.0",
        "wincertstore==0.2",
        "charset-normalizer==3.3.2",
        "colorama==0.4.6",
        "idna==3.6",
    ],

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent'
    ],
    python_requires=">=3.7"
)