# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2024-09-05

### Changed

- Remove `set_units`, pass units of type `units.Units` as a parameter to `get_conditions`
- Drop Python 3.6 support

### Added

- `parse_response` function to transform a raw JSON response string into a `Conditions` object
- `DataStructureType` enum
- Python support until 3.12

## [0.2.1] - 2021-02-04

### Fixed

- Remove temperature conversion for humidity

## [0.2.0] - 2020-12-23

### Added

- CI with GitHub Actions

### Changed

- Remove imports of  `conditions` and `discovery` module in global namespace

### Fixed

- Project links in setup.py

## [0.1.0] - 2020-12-23

Initial public release

[Unreleased]: https://github.com/lukasberbuer/weatherlink-live-local-python/compare/0.3.0...HEAD
[0.3.0]: https://github.com/lukasberbuer/weatherlink-live-local-python/compare/0.2.1...0.3.0
[0.2.1]: https://github.com/lukasberbuer/weatherlink-live-local-python/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/lukasberbuer/weatherlink-live-local-python/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/lukasberbuer/weatherlink-live-local-python/releases/tag/0.1.0
