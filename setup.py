from setuptools import setup, find_packages

setup(
    name="can-bus-monitor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CAN Bus Monitor application using Tkinter for GUI and serial communication.",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "pyserial",
        "tkinter",
    ],
    entry_points={
        'console_scripts': [
            'can-bus-monitor=main:setup_gui',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)