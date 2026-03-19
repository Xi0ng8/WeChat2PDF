# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-03-19

### Added
- **X (Twitter) Support**: Added capability to convert X posts to PDF.
- **New Converter**: `x_converter.py` using Playwright for robust JavaScript rendering and CSS cleaning (removes sidebars, login prompts, etc.).
- **Dispatcher Script**: `run.py` now serves as the main entry point, automatically detecting URL types (WeChat vs X) and routing to the appropriate converter.
- **Skill Update**: Updated `SKILL.md` with new routing instructions for seamless AI integration with X.com and twitter.com links.

### Fixed
- Improved filename sanitization for better compatibility across different operating systems.
- Updated `requirements.txt` to include `playwright` for enhanced rendering capabilities.

## [0.1.2] - 2026-03-13
- Initial release with WeChat to PDF/Markdown conversion support.
