from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent

with open(HERE / "README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

INSTALL_REQUIRES = [
    "zeroconf",
]

EXTRAS_REQUIRE = {
    "docs": [
        "sphinx>=5",
        "sphinx-autodoc-typehints",
        "furo",
        "myst-parser",  # include markdown files
    ],
    "tests": [
        "coverage>=5",  # pyproject.toml support
        "httpretty",
        "pytest>=6",  # pyproject.toml support
    ],
    "tools": [
        "mypy>=0.9",  # pyproject.toml support
        "ruff>=0.5",
        "tox>=3.4",  # pyproject.toml support
    ],
}

EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["docs"] + EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["tools"]
)

setup(
    name="weatherlink-live-local",
    version="0.2.1",
    description="Read current weather data from Davis WeatherLink Live units + connected sensors",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/lukasberbuer/weatherlink-live-local-python",
    author="Lukas Berbuer",
    author_email="lukas.berbuer@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "davis",
        "weatherlink",
        "local",
        "api",
        "weather",
        "iot",
        "smarthome",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    project_urls={
        "Bug Reports": "https://github.com/lukasberbuer/weatherlink-live-local-python/issues",
        "Changelog": "https://github.com/lukasberbuer/weatherlink-live-local-python/blob/master/CHANGELOG.md",
        "Source": "https://github.com/lukasberbuer/weatherlink-live-local-python",
    },
)
