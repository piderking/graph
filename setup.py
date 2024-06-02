from setuptools import setup

setup(
    name="grapher",
    version="0.0.1",
    description="Grapher",
    packages=['graph'],
    package_dir={'':'src'},
    install_requires=['docutils', "requests", "flask", "flask_socketio", "numpy" ]
)