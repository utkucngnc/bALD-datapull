from kadi_apy import KadiManager

from utils import *
from battery import Battery

class KadiInstance():
    """
    Represents an instance of the Kadi system.

    Attributes:
        manager (KadiManager): The Kadi manager object.
        kadiUrl (str): The URL of the Kadi system.
        isCreatedFlag (bool): Flag indicating if the Kadi instance is created.
        isUserValidated (bool): Flag indicating if the user is validated.
        cfg (Config): The configuration object.

    Methods:
        login(cfg): Logs in to the Kadi system.
        userDetails(): Returns the user details.
        getRecordsByTag(tag, save_response, save_items): Retrieves records by tag.
    """

    def __init__(self):
        self.manager = None
        self.kadiUrl = ""
        self.isCreatedFlag = True
        self.isUserValidated = False
        self.cfg = None

    def login(self, cfg):
        """
        Logs in to the Kadi system.

        Args:
            cfg (Config): The configuration object.

        Raises:
            Exception: If the login fails.

        Returns:
            None
        """
        hostUrl = cfg.kadi.main_url
        userToken = cfg.kadi.token_hash
        assert userToken != '', 'No token found, please check your config file'
        
        print('Establishing connection to Kadi...')
        self.manager = KadiManager(host=str(hostUrl), token=str(userToken), verify=False)
        response = self.manager.make_request(endpoint="/users/me", method="get")
        if response.status_code == 200:
            self.isUserValidated = True
            self.user = self.manager.pat_user
            self.cfg = cfg
            print('Connection established')
        else:
            print('Connection failed, please check your token and url')

    def userDetails(self):
        """
        Returns the user details.

        Raises:
            Exception: If user details are not found.

        Returns:
            list: A list containing the user's name and ID.
        """
        if self.cfg is not None:
            return [self.user.name, self.user.id]
        else:
            raise Exception('No user details found, please login first')

    def getRecordsByTag(self, tag: int, save_response=True, save_items=False):
        """
        Retrieves records by tag.

        Args:
            tag (int): The tag of the records to retrieve.
            save_response (bool): Flag indicating whether to save the response as a JSON file.
            save_items (bool): Flag indicating whether to save the retrieved items.

        Raises:
            Exception: If user details are not found.

        Returns:
            list: A list of Battery objects representing the retrieved records.
        """
        if self.cfg is not None:
            endpoint = '/records/' + str(tag) + '/files'
            print(f'Accessing the records: {endpoint}')
            response = self.manager.make_request(endpoint=endpoint, method="get")
            save_json('response.json', response.json()) if save_response else None
            items = response.json()['items']
            if items == []:
                print('No items found')
            else:
                batteries = []
                for i, item in enumerate(items):
                    print('\nFile found: ' + item['name'])
                    if input('Do you want to download this file? (y/n) ') == 'n':
                        continue
                    print('Downloading file...')
                    df = get_file_as_dataframe(self.manager, item)
                    save_dataframe(self.cfg, item, df) if save_items else None
                    batteries.append(Battery(df, item['name']))

                return batteries
        else:
            raise Exception('No user details found, please login first')