import logging
import os
import yaml
import json
import random
import uuid


AIRFLOW_PATH = '/home/ec2-user/airflow/dags'
RUNNER_SUFFIX = '_runner.py'
OWNER = 'aiola@gad-co.ml'
MANIFEST_TYPE = 'yaml'


def main():
    global air_flow_struct, proj_name
    global my_ipynb_j, owner
    global file_to_handle
    file_to_handle = False
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if not file_to_handle or file_to_handle.isspace():
        file_to_handle = 'base.ipynb'
    owner = False
    if not owner or owner.isspace(): owner = OWNER
    logging.debug(f'file to parse {file_to_handle}')
    logging.debug(owner)
    with open(file_to_handle) as my_ipynb, open('basic.yaml') as air_f_t:
        my_ipynb_j = json.loads(my_ipynb.read())
        air_flow_struct = yaml.safe_load(air_f_t.read())
    proj_name = 'generated/'+f_rand_name()
    f_uid = str(uuid.uuid1())
    logging.debug(proj_name)
    logging.debug(f_uid)
    example()


def f_rand_name():
    # animals list from https://gist.githubusercontent.com/atduskgreg/3cf8ef48cb0d29cf151bedad81553a54/raw/82f142562cf50b0f6fb8010f890b2f934093553e/animals.txt
    words_f = 'animals.txt'
    with open(words_f) as l_file:
        l_words=l_file.read().split()
        return random.choice(l_words)


def cre_task(seq=1,operator='airflow.operators.bash_operator.BashOperator',**params):
    """Creating task dict for the dag yaml 
    the keys of the dict is the parameters of the operator as they are in airflow 
        parameters:
            sql: task seq 
        operator: the airflow operator to run """
    return{f'task_{seq}':{'operator':operator} | {key:value for key,value in params.items()}}


def cre_run_file(proj_name='gad_1',base_file="general_runner.py",f_sufix=RUNNER_SUFFIX,dest_loc=AIRFLOW_PATH):    
    with open(f"{base_file}") as tempLate, open(f"{proj_name}{f_sufix}" ,'w') as out_f:
        for n,txt in enumerate(tempLate):
            if n!=3:
                out_f.write(txt)
            else:
                logging.debug(txt)
                out_f.write(txt.replace('/path/to/dags/config_file.yml',f"{dest_loc}/{proj_name}.yml"))
                

def example():
    manifest_dict={}
    # exmple for execution 
    # cre_task(1,operator='airflow.operators.bash_operator.BashOperator',bash_command= 'echo 1',dependencies=['task_1','task_2'])
    cre_task(1,bash_command= 'echo 1',dependencies=['task_1','task_2'])


    #start building the dict
    air_flow_struct[proj_name]=air_flow_struct.pop('example_dag1')
    air_flow_struct[proj_name]['default_args']['owner']=owner
    logging.debug(air_flow_struct)

    #create dedicated dir for all ipynb file 
    try:
        os.makedirs(proj_name, exist_ok=True)
    except Exception as e:
        logging.error(f'unexpected error while creating {proj_name}, {e}')
        raise



    [air_flow_struct[proj_name].pop(x) for x in ['on_success_callback_name','on_success_callback_file','on_failure_callback_name','on_failure_callback_file']]

    logging.debug(air_flow_struct[proj_name].keys())

    #start 
    IMPORT_TAG = 'import'
    inpynb_tmplate = my_ipynb_j.copy()
    inpynb_tmplate['cells']=[]
    import_cells = []
    all_nb = []


    new_nb = inpynb_tmplate.copy()
    new_cells =[]
    first_cell = True

    for n,cell in enumerate(my_ipynb_j['cells']):
        logging.debug(n)
        try:
            if IMPORT_TAG in cell['metadata']['tags']:
                import_cells.append(cell)
                continue
        except KeyError:
            pass
        logging.debug('afetr if 1')
        if first_cell:
            new_cells.append(cell)
            first_cell = False
            logging.debug('in if first')
        else:
            try:
                if new_cells and new_cells[-1]['metadata'] == cell['metadata']:
                    new_cells.append(cell)
                elif new_cells and new_cells[-1]['metadata']['tags'] == cell['metadata']['tags']:
                    new_cells.append(cell)
                else:
                    
                    new_nb['cells'] = import_cells + new_cells
                    all_nb.append(new_nb)
                    print(len(all_nb))
                    new_nb = inpynb_tmplate.copy()
                    new_cells = [cell]
            except KeyError:
                raise
        #the last cell is not line previuse 
    # print(new_cells)
    new_nb['cells'] = import_cells + new_cells
    all_nb.append(new_nb)

    #remove dumy tasks
    del air_flow_struct[proj_name]['tasks']

    logging.debug(f'len of all_nb:{len(all_nb)}')

    prefix = f'{proj_name}/gen_'
    for n,i in enumerate(all_nb):
        f_name = f'{prefix}{file_to_handle.replace(".ipynb","")}{n}.ipynb'
        with open(f_name,'w') as o_f:
            o_f.write(json.dumps(i))
    #     command = f'\'> papermill {AIRFLOW_PATH}/{f_name} {AIRFLOW_PATH}/{proj_name}/out/out_{f_name.split("/")[-1]}\''
        command = f"'{AIRFLOW_PATH}/r.sh {proj_name} {file_to_handle.replace('.ipynb','')} {n}'"
        if n==0:
            air_flow_struct[proj_name]['tasks'] = cre_task(n+1,bash_command=command)
            manifest_dict['files']=[f_name]
        else:
            air_flow_struct[proj_name]['tasks'] = air_flow_struct[proj_name]['tasks'] | cre_task(n+1,bash_command=command,dependencies=f'[task_{n}]')
            manifest_dict['files'].append(f_name)
    manifest_dict['proj_name']=proj_name
    with open(f'{proj_name}_manifest.yml','w') as w_y_p:
        yaml.safe_dump_all(manifest_dict,w_y_p)        

    with open(f"{proj_name}_tmp.yml",'w') as w_y_f :
        yaml.dump(air_flow_struct,w_y_f)
    with open(f"{proj_name}_tmp.yml") as w_y_f, open(f"{proj_name}.yml",'w') as w_o_y_f:
        for n,i in enumerate(w_y_f):
            w_o_y_f.write(i.replace("'''","'").replace("'[","[").replace("]'","]"))
    try:
        os.remove(f"{proj_name}_tmp.yml")
    except:
        logging.error('could not delete tmp file')
        
    cre_run_file(proj_name)

    # os.system(f'say done, ready to run, package {proj_name}')


__main__ = main()
