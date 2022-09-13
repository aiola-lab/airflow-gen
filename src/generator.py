import os
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape
import json
import logging
import uuid

logger = logging.getLogger().setLevel(logging.DEBUG)
env = Environment(
    loader=PackageLoader('airflow'),
    autoescape=select_autoescape()
)

target_dir = os.getenv('TARGET_DIR', 'generated')
conf_file = os.getenv('CONF_FILE', 'dag_params.json')
with open(conf_file) as cf:
    conf = json.load(cf)
    logging.info(f'conf_file: {conf}')
template = env.get_template("airflow.jinja")
files = os.listdir('.')
pynb_files = []
for file in files:
    if file.endswith('.ipynb'):
        pynb_files.append({"path": file, "name": file.replace('.ipynb', '')})
print(pynb_files)

dag_name = f"{pynb_files[0]['name']}_{str(uuid.uuid4())[:8]}"
os.makedirs(target_dir, exist_ok=True)
with open(f"{target_dir}/{dag_name}.py", 'w') as dag:
    dag.write(template.render(conf, dag_name=dag_name, files=pynb_files, current_date=datetime.now()))
# print(template.render(files=pynb_files, owner="land", email="land@airflow", interval='@hourly', current_date=datetime.now()))
