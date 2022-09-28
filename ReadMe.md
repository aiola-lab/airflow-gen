# Airflow DAG Generator

Genderating DAG python file for GAD ML flow
DAG is based on [Jinja Template](https://jinja.palletsprojects.com/)

## Use jupyter notebook extension

1. Install jupyter notebook (under your virtual environment): ```pip install notebook```
2. Install notebook extensions [See this page](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html)
3. Install the generator extension: ```jupyter nbextension install notebook-extention --user```


## Generate DAG using the extension

Once you run ```jupyter notebook``` and open a .ipynb file relies under the base directory, you can find the generated button in the toolbar
When clicked you need to fill the required parameters and click ```Generate```
