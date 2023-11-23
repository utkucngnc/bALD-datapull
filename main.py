from utils import *
from kadi_access import KadiInstance as KI

print('Checking config file...')
cfg = get_config()

token = cfg.kadi.token_hash
host = cfg.kadi.main_url

print('Config file loaded, initializing save folder...')
check_folder(cfg.data.save_path)

print('Save folder initialized, initializing Kadi instance...')
k = KI()
k.login(cfg)

k.getRecordsByTag(1948, save_response=True, save_items=True)