from utils import *
from kadi_access import KadiInstance as KI
from basic_ui import App

print('Checking config file...')
cfg = get_config()

token = cfg.kadi.token_hash
host = cfg.kadi.main_url

print('Config file loaded, initializing save folders...')
check_folder(cfg.data.save_path)
check_folder(cfg.data.plot_path)

print('Save folders initialized, initializing Kadi instance...')
k = KI()
k.login(cfg)

batteries = k.getRecordsByTag(1704, save_response=True, save_items=False)

app = App(batteries, cfg)
app.mainloop()