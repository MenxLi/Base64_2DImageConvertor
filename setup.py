from setuptools import setup, find_packages, Extension
import glob, os

setup(
    name="b64ImConverter",
    version="0.1.0",
    author="Mengxun Li",
    author_email="mengxunli@whu.edu.cn",
    description="Base-64 image converter",

    url="https://github.com/MenxLi/Base64_2DImageConvertor", 

    packages=find_packages(),

    classifiers = [
        "Development Status :: 4",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.5",

    include_package_data = True,

    install_requires = ["numpy"],

	data_files=[
		("b64ImConverter", ["b64ImConverter/c_utils.so", "b64ImConverter/c_utils.dll", "b64ImConverter/c_utils.dylib"])
	]

)