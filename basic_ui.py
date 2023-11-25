import customtkinter

class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()

class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item):
        button = customtkinter.CTkButton(self, text=item, width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=15)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


class App(customtkinter.CTk):
    """
    This class represents the main application window for Kadi Battery Analysis.

    Args:
        data (list): List of battery objects.
        cfg (object): Configuration object.

    Attributes:
        data (list): List of battery objects.
        battery_names (list): List of battery names.
        figure_save_path (str): Path to save the figures.
        current_obj (object): Currently selected battery object.
        button_config (list): List of button configurations.

    Methods:
        checkbox_frame_event: Event handler for checkbox frame modification.
        radiobutton_frame_event: Event handler for radiobutton frame modification.
        label_button_frame_event: Event handler for label and button frame events.
    """

    def __init__(self, data, cfg):
        super().__init__()
        self.data = data
        self.battery_names = [battery.name for battery in self.data]
        self.figure_save_path = cfg.data.plot_path
        self.current_obj = None

        self.title("Kadi Battery Analysis")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)
        self.button_config = ['Plot', 'Plot & Save', 'Export Data']

        # create scrollable radiobutton frame for battery selection
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                                                                       item_list=[i for i in self.battery_names],
                                                                       label_text="Measurements")
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=200)
        
        # create scrollable label and button frame
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=300, command=self.label_button_frame_event, corner_radius=0)
        self.scrollable_label_button_frame.grid(row=0, column=3, padx=15, pady=15, sticky="nsew")
        for i in self.button_config:  # add items with images
            self.scrollable_label_button_frame.add_item(i)

    def checkbox_frame_event(self):
        """
        Event handler for checkbox frame modification.
        Prints the checked items in the checkbox frame.
        """
        print(f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")

    def radiobutton_frame_event(self):
        """
        Event handler for radiobutton frame modification.
        Updates the current_obj and step_ids attributes based on the selected measurement.
        """
        self.current_obj = self.data[self.battery_names.index(self.scrollable_radiobutton_frame.get_checked_item())]
        self.step_ids = self.current_obj.step_ids
        self.columns = self.current_obj.columns
        print(f"Selected measurement changed: {self.scrollable_radiobutton_frame.get_checked_item()}")

        # create scrollable radiobutton frame for step selection
        self.scrollable_radiobutton_frame2 = ScrollableRadiobuttonFrame(master=self, width=500, command=None,
                                                                    item_list=self.step_ids,
                                                                    label_text="Select Step")
        self.scrollable_radiobutton_frame2.grid(row=0, column=1, padx=15, pady=15, sticky="ns")
        self.scrollable_radiobutton_frame2.configure(width=200)

        # create scrollable checkbox frame
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200, command=self.checkbox_frame_event,
                                                                 item_list=self.columns)
        self.scrollable_checkbox_frame.grid(row=0, column=2, padx=15, pady=15, sticky="ns")

    def label_button_frame_event(self, item):
        """
        Event handler for label and button frame events.
        Prints the current step and performs actions based on the selected item and checked columns.
        
        Args:
            item (str): Selected item from the label and button frame.
        """
        current_step = int(self.scrollable_radiobutton_frame2.get_checked_item())
        if current_step is None:
            print('Please select a step')
            return
        else:
            print(f'Current step: {current_step}')
            if len(self.scrollable_checkbox_frame.get_checked_items()) == 2:
                x, y = self.scrollable_checkbox_frame.get_checked_items()
                if item == 'Plot':
                    self.current_obj.plot(current_step, x, y, save_path=None)
                    return
                elif item == 'Plot & Save':
                    self.current_obj.plot(int(self.scrollable_radiobutton_frame2.get_checked_item()), x, y, save=self.figure_save_path)
                    return
                elif item == 'Export Data':
                    self.current_obj.save_partial_df(self.figure_save_path)
                    return
            elif len(self.scrollable_checkbox_frame.get_checked_items()) > 2:
                print("Too many variables are selected")
                return
            else:
                print("No columns selected")
                return
                