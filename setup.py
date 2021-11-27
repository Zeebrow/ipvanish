from setuptools import setup, find_packages

setup(
    name='ipvanish',
    version='0.0.1',
    package_dir={'':'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'Click'
    ],
    entry_points={'console_scripts':[
            'ipvanish = scripts.ipvanish:main',
            'nmclpy = scripts.nmclipy:main',
        ],
    },
)
