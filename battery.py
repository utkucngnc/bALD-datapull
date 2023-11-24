import pandas as pd
import matplotlib.pyplot as plt

class Battery():
    def __init__(self, df: pd.DataFrame, name: str) -> None:
        self.df = df
        self.columns = df.columns
        self.name = name
        self.step_ids = self.df['Step ID'].unique()
        self.partial_df = None

    def plot(self, step_id: int, x: str, y: str, save_path: None) -> None:
        self.partial_df = self.get_partial_df(step_id)
        assert self.df[x].shape == self.df[y].shape, 'x and y must have the same shape'
        assert x in self.columns, f'Column {x} not found'
        assert y in self.columns, f'Column {y} not found'
        
        title = f'{x} vs {y} (Step ID: {step_id}), Step Type: {self.partial_df["Step Type"].values[0]}'
        self.partial_df.plot(x=x, y=y, kind='line', title=title, xlabel=x, ylabel=y)
        if save_path:
            plt.savefig(save_path + title + '.png')
        plt.show()
    
    def get_partial_df(self, step_id: int) -> pd.DataFrame:
        assert not self.df[self.df['Step ID'] == step_id].empty, f'Step ID {step_id} not found'
        return self.df[self.df['Step ID'] == step_id]
    
    def save_partial_df(self, save_path: str) -> None:
        self.partial_df.to_csv(save_path, index=False, sep='\t', mode='a')