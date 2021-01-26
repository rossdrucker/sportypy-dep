# -*- coding: utf-8 -*-
'''
Data Management Utilities

Author: Federico Scivittaro

Date: 6/28/17

Contains utility functions applicable to all files. Functions are responsible
for making requests to a server and for performing basic data storage and
management.

UPDATE 12/13/17 by Dylan Schultz
Added open_SQL_to_df function
'''

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import ConnectionError, Timeout

from bs4 import BeautifulSoup
import time
import pandas as pd
import json
import pypyodbc
from jellyfish import jaro_winkler
from sqlalchemy import create_engine

def prepare_request(num_retries=10, timeout=3.1):
    '''
    Returns a prepared request with mounted retry and timeout parameters. The
    request will try to access the server num_retries times before returning an
    exception and will timeout after timeout seconds (by convention timeout is
    set to slightly larger than a multiple of 3). A timeout will prompt a
    retry.
    '''

    req = requests.Session()

    retries = Retry(total = num_retries,
                    backoff_factor = 10, # Delay of 10 seconds
                    status_forcelist = [500, 502, 503, 504])

    req.mount('http://', HTTPAdapter(max_retries = retries)) # Mount the retry
    req.mount('https://', HTTPAdapter(max_retries = retries))

    # Create class capable of mounting timeouts
    class TimeoutAdapter(HTTPAdapter):
        def __init__(self, timeout=None, *args, **kwargs):
            self.timeout = timeout
            super(TimeoutAdapter, self).__init__(*args, **kwargs)

        def send(self, *args, **kwargs):
            kwargs['timeout'] = self.timeout
            return super(TimeoutAdapter, self).send(*args, **kwargs)


    req.mount('http://', TimeoutAdapter(timeout=timeout)) # Mount the timeout
    req.mount('https://', TimeoutAdapter(timeout=timeout))

    return req


def make_robust_request(url, num_retries=10, timeout=3.1, headers=None,
                        params=None, proxies=None):
    '''
    Tries to send a request and return a response from the server. Will sleep
    for 60 seconds and then try again (up to ten times) in the case of a
    Connection Error or Read Timeout error.
    '''

    req = prepare_request(num_retries, timeout)
    attempts = 0

    while attempts < num_retries: # Max of 10 attempts before failing
        try:
            response = req.get(url, headers=headers, params=params,
                               proxies=proxies)
            break
        except (ConnectionError, Timeout) as error:
            print(str(error) + ' -- waiting 30 seconds')
            attempts += 1
            time.sleep(30) # Give some time before trying again
        except:
            raise

    return response


def get_soup(url, num_retries=10, timeout=3.1, proxies=None):
    '''
    Tries to send a BeautifulSoup request and return a response from the
    server. Will sleep for 60 seconds and then try again (up to ten times) in
    the case of a Connection Error or Read Timeout error.
    '''

    req = prepare_request(num_retries, timeout)

    attempts = 0

    while attempts < 10: # Max of 10 attempts before failing
        try:
            soup = BeautifulSoup(req.get(url, proxies=proxies).text,
                                 'html.parser')
            break
        except (ConnectionError, Timeout) as error:
            print(str(error) + ' -- waiting 30 seconds')
            attempts += 1
            time.sleep(30) # Give some time before trying again
        except:
            raise

    return soup


def save_df_to_csv(df, filename, sep='|', col_headers=True, index=False,
                   index_label=None, mode='a'):
    '''
    Saves the df to a csv file.
    '''

    if not df.empty:
        df.to_csv(filename, sep=sep, header=col_headers, index=index,
                  index_label=index_label, mode=mode, encoding='utf-8')

    return None


def open_csv_to_df(filename, index=None, dtype=None):
    '''
    Loads a CSV file and returns it as a Pandas df.
    '''

    df = pd.read_csv(filename, sep='|', header=0, index_col=index,
                     encoding='utf-8', dtype=dtype)

    return df

def open_SQL_to_df(server, database, query):
    '''
    Loads a table from SQL into a Pandas df. 
    '''

    connection = pypyodbc.connect('Driver=SQL Server;\
                                  Server={};\
                                  Database={}'.format(server, database))
    
    df = pd.read_sql_query(query, connection)
    
    return df

def save_df_to_SQL(df, tableName, server, database, dtypes=None, mode='fail'):
    '''
    Saves the df to a SQL server table.
    
    mode specifies what to do if table exists.  Options are fail, replace,
    or append.
    
    dtypes should be a dictionary of column_name : SQL_type
    '''
    engine = create_engine('mssql+pyodbc://@{}/{}?driver=SQL+Server'\
                           .format(server, database), echo=False)
    
    df.to_sql(tableName, con=engine, if_exists=mode, index=False, dtype=dtypes)

def find_match(name, compare_list):
    '''
    Iterate through a list of strings to find the best match for the given
    string using Jaro-Winkler distance, a more sophisticated calculation
    than Levenshtein distance.
    '''

    max_dist = 0
    match = None

    for comparison in compare_list:
        dist = jaro_winkler(u'{}'.format(name), u'{}'.format(comparison))

        if dist > max_dist:
            match = comparison
            max_dist = dist

    return match

def get_api_keys(application,
                 key_file='S:/Everyone/Products/API_keys/api_keys.json'):
        '''
        Reads the api key file in and gets the keys for the proper app.
        '''
        
        with open(key_file, 'r') as f:
            json_string = f.read()
        
        all_keys = json.loads(json_string)
        
        try:
            keys = all_keys[application]
            return keys
        
        except KeyError:
            print('Application name not in file')
            return
        
        
