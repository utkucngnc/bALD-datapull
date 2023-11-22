from utils import *

cfg = get_config()
df = read_excel(cfg.data.xlsx_path)

print(df.columns)