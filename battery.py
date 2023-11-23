import pandas as pd
import matplotlib.pyplot as plt

class Battery():
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.columns = df.columns

    def plot(self, x: str, y: str, title: str, xlabel: str, ylabel: str, save: bool = False, save_path: str = None) -> None:
        assert self.df[x].shape == self.df[y].shape, 'x and y must have the same shape'
        assert x in self.columns, f'Column {x} not found'
        if self.check_column(x) == 'time':
            self.convert_datetime(x)
        elif self.check_column(x) == 'numeric':
            self.convert_float(x)
        else:
            assert False, f'Column {x} must be numeric or time'

        assert y in self.columns, f'Column {y} not found'
        if self.check_column(y) == 'time':
            self.convert_datetime(y)
        elif self.check_column(y) == 'numeric':
            self.convert_float(y)
        else:
            assert False, f'Column {y} must be numeric or time'

        plt.plot(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        if save:
            assert save_path != None, 'save_path must be given'
            plt.savefig(save_path)
        plt.show()
    
    def check_column(self, column: str) -> None:
        assert column in self.columns, f'Column {column} not found'
        temp = self.df[column][0]

        if isinstance(temp, float):
            return 'numeric'
        else:
            if ':' in temp:
                return 'time'
            else:
                return 'nan'
    
    def convert_float(self, column: str) -> None:
        assert column in self.columns, f'Column {column} not found'
        self.df[column] = self.df[column].astype(float)
    
    def convert_datetime(self, column: str) -> None:
        assert column in self.columns, f'Column {column} not found'
        self.df[column] = pd.to_datetime(self.df[column])