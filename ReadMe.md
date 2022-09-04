# Airflow DAG Generator

Genderating DAG python file for GAD ML flow
DAG is based on [Jinja Template](https://jinja.palletsprojects.com/)

## Howto Use

1. Update dag_params.json
2. Execute `python src/generator.py`

## Use jupyter notebook extension

1. Install jupyter notebook (under your virtual environment): ```pip install notebook```
2. Install notebook extensions [See this page](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html)
3. Install the generator extension: ```jupyter nbextension install notebook-extention --user```
