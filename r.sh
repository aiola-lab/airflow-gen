#!/bin/bash
papermill /home/ec2-user/airflow/dags/$1/gen_$2$3.ipynb /home/ec2-user/airflow/dags/out/out_$1$2$3.ipynb
