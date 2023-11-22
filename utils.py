from omegaconf import OmegaConf
import pandas as pd

def get_config(config_path: str = "config.yaml"):
    config = OmegaConf.load(config_path)
    return config

def read_csv(path):
    data = pd.read_csv(path, sheet_name = 0, engine='openpyxl')
    return data

def read_excel(path):
    data = pd.read_excel(path)
    return data