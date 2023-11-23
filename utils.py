from omegaconf import OmegaConf
import pandas as pd
import json
import io
import os

def get_config(config_path: str = "config.yaml"):
    config = OmegaConf.load(config_path)
    return config

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

def read_response(response):
    with io.BytesIO(response.content) as fh:
        df = pd.io.excel.read_excel(fh, engine='openpyxl')
    
    return df

def get_file_as_dataframe(manager, download_url: str):
    try:
        response = manager.make_request(endpoint=download_url, method="get")
        return read_response(response)
    except:
        raise Exception('Error while downloading file, check KadiManager connection')