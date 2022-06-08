#!/usr/bin/env python

import os

from setuptools import setup

setup(name='NSX SDK',
    version='3.1.2',
    description='NSX SDK for Python',
    packages=['lib'],
    include_package_data=True,
    package_data={
        'lib': ['*.whl'],
    },
    install_requires=[
        'vapi-runtime @ file://localhost/{}/lib/vapi_runtime-2.19.0-py2.py3-none-any.whl'.format(os.getcwd()),
        'vapi-client-bindings @ file://localhost/{}/lib/vapi_common_client-2.19.0-py2.py3-none-any.whl'.format(os.getcwd()),
        'vapi-common-client @ file://localhost/{}/lib/vapi_common-2.19.0-py2.py3-none-any.whl'.format(os.getcwd()),
        'nsx-python-sdk @ file://localhost/{}/lib/nsx_python_sdk-3.1.2.0.0-py2.py3-none-any.whl'.format(os.getcwd()),
        'nsx-policy-python-sdk @ file://localhost/{}/lib/nsx_policy_python_sdk-3.1.2.0.0-py2.py3-none-any.whl'.format(os.getcwd()),
    ],
    classifiers=[
        "Development Status :: 5 - Production / Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: ADEO License",
        "Programming Language :: Python :: 3",
    ]
)