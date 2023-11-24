import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime

from utils import *


df = read_excel('./example_data/example.xlsx')
print(df[df['Step ID'] == 0])
'''
df.plot(x='Time', y='Voltage(V)',kind='line', figsize=(10,10))

plt.show()
'''