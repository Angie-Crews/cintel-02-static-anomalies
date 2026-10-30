# cintel-02-static-anomalies

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](pyproject.toml)
[![CI](https://github.com/Angie-Crews/cintel-02-static-anomalies/actions/workflows/ci-python-zensical.yml/badge.svg)](https://github.com/Angie-Crews/cintel-02-static-anomalies/actions/workflows/ci-python-zensical.yml)
[![Documentation](https://img.shields.io/badge/docs-site-blue?logo=github)](https://angie-crews.github.io/cintel-02-static-anomalies/)

[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

 > Detect unusually large Missouri state travel expenditures using static anomaly detection.

## Project Overview

Author: Angie Crews

Date: 2026 October

This project analyzes 2026 Missouri state expenditure data to identify
unusually large travel expenditures that may warrant further review.

The project uses static anomaly detection to flag travel payments that
are unusually high compared with other travel expenditures.

The project is configured in
[pyproject.toml](pyproject.toml).

## Data

This project uses the
[2026 Missouri State Expenditures dataset](https://data.mo.gov/Government-Administration/2026-State-Expenditures/gndj-tfr3/about_data)
from the Missouri Data Portal.

The dataset contains 102,540 expenditure records with information including:

- Fiscal Year
- Agency Name
- Category Description
- Detail Description
- Vendor Name
- Payments Total

For this project, I focused on the 37,402 records categorized as
travel expenditures.

## Approach

The project uses Polars to load and clean the Missouri expenditure data.

The analysis:

- Converts payment amounts to numeric values.
- Filters the data to include only travel expenditures.
- Calculates the 99th percentile of travel payments.
- Uses the 99th percentile as the anomaly threshold.
- Flags unusually large travel expenditures for further review.
- Summarizes the flagged expenditures by state agency.
- Creates a visualization of the top 10 agencies by number of flagged expenditures.

Explore these project components:

- [pyproject.toml](pyproject.toml) - project configuration and dependencies.
- [src/cintel/expenditure_anomaly_detector.py](src/cintel/expenditure_anomaly_detector.py) - custom anomaly detection pipeline.
- [data/](data/) - input data.
- [artifacts/](artifacts/) - generated anomaly results.
- [docs/](docs/) - project documentation and visualization.
- [tests/](tests/) - automated tests.
- [.github/workflows/](.github/workflows/) - automated checks and documentation deployment.

## Run the Project

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
to set up your machine and project environment.

Download the
[2026 Missouri State Expenditures dataset](https://data.mo.gov/Government-Administration/2026-State-Expenditures/gndj-tfr3/about_data)
and save the CSV file in the `data/` folder.

From a VS Code terminal in the project root, run:

```shell
uv run python -m cintel.expenditure_anomaly_detector
```

## Results

The analysis identified 404 unusually large travel expenditures
across 23 Missouri state agencies.

The 99th percentile of travel payments was $10,110.40.
Travel expenditures at or above this amount were flagged for further review.

The Legislature had the highest number of flagged travel expenditures.

The flagged records are saved to:

`artifacts/missouri_travel_anomalies.csv`

The project also creates a visualization showing the top 10 agencies
by number of flagged travel expenditures:

`docs/images/travel_anomalies_by_agency.png`

A flagged expenditure does not necessarily indicate an error or improper
spending. It only indicates that the payment was unusually large based
on the threshold used in this analysis.

## Verification

Run the automated tests:

```shell
uv run pytest
```

## Project Documentation

The [hosted documentation site](https://angie-crews.github.io/cintel-02-static-anomalies/)
is published using Zensical and GitHub Pages.

The documentation presents the Missouri travel expenditure analysis,
including the data, methods, results, visualization, interpretation,
and conclusions.

## CI/CD and GitHub Actions

This project includes continuous integration and continuous deployment (CI/CD)
to check project files and publish the documentation.

GitHub Actions include:

- [CI: Python and Documentation Checks](https://github.com/Angie-Crews/cintel-02-static-anomalies/actions/workflows/ci-python-zensical.yml)
- [CD: Documentation Deployment](https://github.com/Angie-Crews/cintel-02-static-anomalies/actions/workflows/deploy-zensical.yml)

## Developer Reference

Follow the
[Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
for **detailed instructions and troubleshooting**.

### Initialize and Update the Python Environment

With the project open in VS Code, open a VS Code terminal.
Paste each command and hit Enter or Return after to run it.

```shell
uvx pup-clean --delete
uv self update
uv python pin 3.14
uv python install
uv lock --upgrade
uv sync
uv audit
```

### Set Up and Run Git Hooks

Set up and run the git hooks to perform
basic checks automatically before
any changes get pushed to GitHub.

In the VS Code terminal,
paste each command and hit Enter or Return after to run it.

```shell
uvx prek install --force
uvx prek update --freeze --cooldown-days 7

git add -A
uvx prek run --all-files
# repeat if changes were made
uvx prek run --all-files
```

### Run Common Chores

Run linters, formatters, type checks, tests, and
build the documentation.

```shell
uv run ruff check . --fix
uv run ruff format .

uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

### Git add-commit-push to GitHub

After making useful changes, save your work to GitHub.

```shell
git add -A
git commit -m "describe your changes in quotes"
git push -u origin main
```

## Developer Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.

## Developer Tools

This project uses professional Python tools to support development,
testing, documentation, and code quality.

- [uv](https://docs.astral.sh/uv/) - Python environments and dependencies.
- [Ruff](https://docs.astral.sh/ruff/) - Python linting and formatting, configured in [.ruff.toml](.ruff.toml).
- [ty](https://docs.astral.sh/ty/) - Python type checking.
- [pytest](https://docs.pytest.org/) - automated Python testing, configured in [.pytest.toml](.pytest.toml).
- [prek](https://prek.j178.dev/) - Git hooks and automated checks, configured in [prek.toml](prek.toml).
- [Zensical](https://zensical.org/) - project documentation, configured in [zensical.toml](zensical.toml).

## Links

- [Hosted Documentation](https://angie-crews.github.io/cintel-02-static-anomalies/)
- [2026 Missouri State Expenditures Dataset](https://data.mo.gov/Government-Administration/2026-State-Expenditures/gndj-tfr3/about_data)
- [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
- [Citation](CITATION.cff)
- [License](LICENSE)
