# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0]
### Changed
- Storage changed from MongoDB (mongoengine) to PostgreSQL (SQLAlchemy).
- Discord user data now is `msg.frm.fullname` to `username` field.


## [1.1.0]
### Added
- Added field `type`, now liquid are stored in same collection, with no restriction in described in string `type`

### Removed
- Remove `provider` field from model and in the models already stored.


## [1.0.0]
### Added
- Add docstrings to classes and methods.
- Readme update with stored schema explained.
- Commands example.


## [0.3.0]
### Added
- Tests to commands `!maya liquid add`, `!maya liquid list` and `!maya liquid remove`.
- Parameter `--date` to `!maya liquid add` using ISO 8601 to specify the date and time when the registration should be done.


## [0.2.0]
### Added
- Support to bandit, flake8, isort and pylint.
- Support to Github Actions with matrix to linters and vulnerability checkers.


## [0.1.0]
### Added
- Remove document based on UUID
- List amount of liquid consumed in the day, with command `liquid list` (UTC).


## [0.0.2]
### Added
- Create User model

### Changed
- Command `liquid add`, now stores the user data of the Discord sending, based on parameter `msg.frm.*` as `person`, `nick`, `fullname`, `client`, `email` in model `User`.
- Environment variables now use the `ERR_MAYA_` prefix, to differentiate from duplicate use of other plugins.


## [0.0.1]
### Added
- Create base models (`Client`, `Coffee`, `Liquid`, `Provider`, `Water`).
- Create `liquid add` command.
