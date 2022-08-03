#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='paymentez',
    version='1.0.0',
    author='Preki',
    author_email='kevin@preki.com',
    packages=['paymentez', 'paymentez.models', 'paymentez.utils'],
    url='https://preki.com',
    download_url='https://github.com/GoPreki/PaymentezSDK',
    license='MIT',
    description='Python library for handling Paymentez integration',
    long_description='Python library for handling Paymentez integration',
    install_requires=[
        'requests >= 2.24.0',
    ],
)
