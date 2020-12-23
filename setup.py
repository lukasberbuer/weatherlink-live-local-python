from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent

with open(HERE / "README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

INSTALL_REQUIRES = [
    "zeroconf",
    "dataclasses>=0.6; python_version<'3.7'", 
]

EXTRAS_REQUIRE = {
    "docs": [
        "sphinx>3.1",
        "sphinx-autodoc-typehints",
        "sphinx-rtd-theme",
        "m2r2",  # include markdown files
    ],
    "tests": [
        "coverage>=5",  # pyproject.toml support
        "httpretty",
        "pytest>=6",  # pyproject.toml support
    ],
    "tools": [
        "black",
        "isort",
        "mypy",
        "pylint>=2.5",  # pyproject.toml support
        "tox>=3.4",  # pyproject.toml support
    ],
}

EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["docs"] + EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["tools"]

setup(
    name="weatherlink_live_local",
    version="0.1.0",
    description="Read current weather data from Davis® WeatherLink Live units + connected sensors",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/vallen-systems/pyWaveline",
    author="Lukas Berbuer",
    author_email="lukas.berbuer@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "Davis",
        "WeatherLink",
        "local",
        "API",
        "weather",
        "IoT",
        "Smart Home",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    project_urls={
        "Bug Reports": "https://github.com/vallen-systems/pyWaveline/issues",
        "Source": "https://github.com/vallen-systems/pyWaveline",
    },
)
