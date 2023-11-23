from omegaconf import OmegaConf
import pandas as pd
import json
import io
import os

def get_config(config_path: str = "config.yaml"):
    config = OmegaConf.load(config_path)
    return config

def check_dtype(fname: str):
    if fname.endswith('.csv'):
        return 'csv'
    elif fname.endswith('.xlsx'):
        return 'xlsx'
    elif fname.endswith('.xls'):
        return 'xls'
    elif fname.endswith('.txt'):
        return 'txt'
    else:
        raise Exception('File type not supported')

def read_csv(path):
    data = pd.read_csv(path, sheet_name = 0, engine='openpyxl')
    return data

def read_excel(path):
    data = pd.read_excel(path)
    return data

def save_json(path: str, data: dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def save_excel(path: str, filename: str, data: pd.DataFrame):
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        data.to_excel(path + filename, index=False, engine='openpyxl')
    except:
        raise Exception('Error while saving data file')

def read_response_excel(response):
    with io.BytesIO(response.content) as fh:
        df = pd.io.excel.read_excel(fh, engine='openpyxl')
    
    return df

def read_response_csv(response):
    with io.StringIO(response.content.decode('utf-8')) as fh:
        df = pd.read_csv(fh)
    
    return df

def read_response_txt(response):
    with io.StringIO(response.content) as fh:
        df = pd.io
    
    return df

def get_file_as_dataframe(manager, item):
    try:
        download_url = item['_links']['download']
        response = manager.make_request(endpoint=download_url, method="get")
        if response.status_code != 200:
            raise Exception('Error while downloading file, check KadiManager connection')
        dtype = check_dtype(item['name'])
        if dtype == 'xls' or dtype == 'xlsx':
            print('Reading excel file...')
            return read_response_excel(response)
        elif dtype == 'csv':
            print('Reading csv file...')
            return read_response_csv(response)
        elif dtype == 'txt':
            print('Reading text file...')
            return read_response_txt(response)
        else:
            raise Exception('File type not supported')
    except:
        raise Exception('Error while downloading file, check KadiManager connection')