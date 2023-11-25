from utils import *
from kadi_access import KadiInstance as KI
from basic_ui import App

def main():
    """
    This script initializes and runs the bALD-datapull application.
    It loads the configuration file, initializes save folders, creates a Kadi instance,
    retrieves battery records using a specific tag, and starts the application's main loop.
    """
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

if __name__ == "__main__":
    main()
