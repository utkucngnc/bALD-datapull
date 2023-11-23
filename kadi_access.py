from kadi_apy import KadiManager
from kadi_apy.lib import resources
from kadi_apy.lib.resources import records
from kadi_apy.lib.resources.users import User
import urllib.request
import json
import logging
from tqdm import tqdm
import io

from datetime import date
from datetime import time
from datetime import datetime

from utils import *

class KadiInstance():
    def __init__(self):
        self.manager = None

        self.kadiUrl = ""
        self.isCreatedFlag = True
        self.isUserValidated = False

    def login(self,hostUrl: str,userToken :str):
        print('Establisihing connection to Kadi...')
        self.manager = KadiManager(host=str(hostUrl), token=str(userToken), verify=False)
        response = self.manager.make_request(endpoint="/users/me", method="get")
        if response.status_code == 200:
            self.isUserValidated = True
            self.user = self.manager.pat_user
            print('Connection established')
        else:
            print('Connection failed, please check your token and url')

    def userDetails(self):
        return [self.user.name,self.user.id]
    
    def getRecordsByTag(self, tag: int, save = True):
        endpoint = '/records/' + str(tag) + '/files'
        print(endpoint)
        response = self.manager.make_request(endpoint=endpoint, method="get")
        items = response.json()['items']
        for _,item in enumerate(tqdm(items)):
            download_url = item['_links']['download']
            df = get_file_as_dataframe(self.manager,download_url)
            save_excel('./data/',item['name'],df) if save else None


if __name__ == '__main__':
    k = KadiInstance()
    cfg = get_config()
    token = cfg.kadi.token_hash
    host = cfg.kadi.main_url
    k.login(host,token)
    k.getRecordsByTag(1704)
    #print(k.userDetails())