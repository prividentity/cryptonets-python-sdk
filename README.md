## CryptoNets Python SDK

## Project description

This package provides an interface to CryptoNets™ 1:N homomorphic token (HT) face recognition, Ultrapass™
ID and human age estimation.

## Getting Started

Sign up on the waitlist on https://private.id to obtain your apiKey.

## Requirements

- Python >= 3.6

## Notices

Licensing Restriction: This SDK is not licensed for use without the consent of the Private Identity.

## Installation

Installation of the CryptoNets Python SDK and its dependencies is provided by `pip`.
If pip is not installed, see the [pip user guide](https://pip.pypa.io/en/stable/installing/ "pip User Guide") to install
pip.

To ensure smooth installation, it’s recommended to use:

- `pip: 9.0.2` or greater

The safest way to install the SDK is to use pip in a virtualenv:

```
python -m pip install cryptonets_python_sdk
```

If you have the cryptonets_python_sdk package installed and want to upgrade to the latest version, you can run:

```
python -m pip install --upgrade cryptonets_python_sdk
```

This will install the cryptonets_python_sdk package as well as all dependencies.
See the [installation](https://privid-sdk.s3.us-east-2.amazonaws.com/cryptonets-python-sdk/1.3.11/installation.html) section of
the SDK homepage Guide for more information.

## Usage

You will receive the Server URL and apiKey when you subscribe.

### Import Face factor

`from cryptonets_python_sdk.factor import FaceFactor`

`from cryptonets_python_sdk.settings.loggingLevel import LoggingLevel`

### Initialize and use factor

```
server_url = URL of the server

api_key = APIKEY issued on successful signup

server = FaceFactor(url=server_url, api_key=api_key,
        logging_level=LoggingLevel.full)
```

## License

[Private Identity License](https://github.com/openinfer/PrivateIdentity/blob/e19cb4870048f14e04a6be99d3cab78f4d8c6360/images/AWS%20EULA%20Template%20(2020.11.20)%20(Private%20Identity).pdf)
Copyright (c) 2020-present, Private Identity All rights reserved.

## More Resources:

[Getting Started](https://privid-sdk.s3.us-east-2.amazonaws.com/cryptonets-python-sdk/1.3.11/index.html#getting-started)

[Installation](https://privid-sdk.s3.us-east-2.amazonaws.com/cryptonets-python-sdk/1.3.11/installation.html)

[Usage](https://privid-sdk.s3.us-east-2.amazonaws.com/cryptonets-python-sdk/1.3.11/usage.html)

[SDK-Docs](https://privid-sdk.s3.us-east-2.amazonaws.com/cryptonets-python-sdk/1.3.11/Factor/Face.html#cryptonets_python_sdk.factor.FaceFactor)