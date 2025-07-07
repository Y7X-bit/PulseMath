from setuptools import setup

setup(
    name="SmartCalculatorGUI",
    version="1.0",
    description="An AMOLED + RedX glow GUI calculator",
    author="Yugank",
    packages=["."],
    install_requires=["customtkinter", "pygame", "matplotlib"],
)
