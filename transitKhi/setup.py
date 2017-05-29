from setuptools import setup

setup(
    name='transitKhi',
    packages=['transitKhi'],
    include_package_data=True,
    install_requires=[
        'flask', 'wtforms','smtplib', 'gmplot', 'numpy', 'networkx', 'csv', 'math','requests', 'urllib',
        'matplotlib.pyplot', 'json', 'io','fuzzywuzzy', 'urllib.request'
    ],
)

