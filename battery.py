import pandas as pd
import matplotlib.pyplot as plt

class Battery():
    def __init__(self, df: pd.DataFrame, name: str) -> None:
        """
        Initializes a Battery object.

        Args:
            df (pd.DataFrame): The DataFrame containing battery data.
            name (str): The name of the battery.
        """
        self.df = df
        self.columns = df.columns
        self.name = name
        self.step_ids = self.df['Step ID'].unique()
        self.partial_df = None

    def plot(self, step_id: int, x: str, y: str, save_path: None) -> None:
        """
        Plots a line graph of the specified x and y columns for a given step ID.

        Args:
            step_id (int): The step ID.
            x (str): The column name for the x-axis.
            y (str): The column name for the y-axis.
            save_path (None or str): The path to save the plot. If None, the plot will be displayed but not saved.
        """
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
        """
        Returns a partial DataFrame for the specified step ID.

        Args:
            step_id (int): The step ID.

        Returns:
            pd.DataFrame: The partial DataFrame containing data for the specified step ID.
        """
        assert not self.df[self.df['Step ID'] == step_id].empty, f'Step ID {step_id} not found'
        return self.df[self.df['Step ID'] == step_id]
    
    def save_partial_df(self, save_path: str) -> None:
        """
        Saves the partial DataFrame to a CSV file.

        Args:
            save_path (str): The path to save the CSV file.
        """
        self.partial_df.to_csv(save_path, index=False, sep='\t', mode='a')