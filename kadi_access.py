from kadi_apy import KadiManager
from tqdm import tqdm

from utils import *

class KadiInstance():
    def __init__(self):
        self.manager = None

        self.kadiUrl = ""
        self.isCreatedFlag = True
        self.isUserValidated = False
        self.cfg = None

    def login(self, cfg):
        hostUrl = cfg.kadi.main_url
        userToken = cfg.kadi.token_hash

        print('Establisihing connection to Kadi...')
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
        if self.cfg is not None:
            return [self.user.name,self.user.id]
        else:
            raise Exception('No user details found, please login first')
    
    def getRecordsByTag(self, tag: int, save_response = True, save_items = False):
        if self.cfg is not None:
            endpoint = '/records/' + str(tag) + '/files'
            print(f'Accessing the records: {endpoint}')
            response = self.manager.make_request(endpoint=endpoint, method="get")
            save_json('response.json',response.json()) if save_response else None
            items = response.json()['items']
            if items == []:
                print('No items found')
            else:
                for _,item in enumerate(tqdm(items)):
                    df = get_file_as_dataframe(self.manager,item)
                    save_dataframe(self.cfg,item,df) if save_items else None
                    break
        else:
            raise Exception('No user details found, please login first')