import pandas as pd


class Battery:
    def __init__(
                self,
                df: pd.DataFrame,
                specs: list
                ) -> None:
        self.df = df
        self.specs = specs
        self.current = self.read_current()
        self.voltage = self.read_voltage()
        self.time = self.read_time()
    
    def read_current(self):
        return self.df["Current"]
    
    def read_voltage(self):
        return self.df["Voltage"]
    
    def plot(self, x, y):
