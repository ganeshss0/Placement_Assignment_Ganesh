##############################
###### Python Answer 3 #######
##############################

# A program to download the data from the link and then read the data and convert the into
# the proper structure and return it as a excel file.





##############################
########## Solution ##########
##############################

# importing urllib3 library for making https requests
# json5 for converting json into dictionary

from urllib3 import PoolManager, exceptions
import numpy as np
import pandas as pd
from json5 import loads
import logging

# basic logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def json_to_excel(url: str, file_name: str):
    '''Download json data from url and write data to given file_name after convert json in csv.'''

    https = PoolManager()

    # sending https request to given url
    logging.info(f'Sending Request to {url}')
    response = https.request(method='GET', url=url)

    # checking the response
    if response.status == 200:
        logging.info('Sending Request Success')
        try:
            # loading the json data into python dictionary
            logging.info('Decoding Raw Data')
            raw_data = response.data.decode()[15:-3]

            # reading data into pandas dataframe
            logging.info('Reading Raw Data')
            df = pd.read_json(raw_data)

            logging.info('Formatting the Data')
            # splitting the type column
            type_col = df.type.apply(pd.Series)
            type_col.columns = 'type_' + type_col.columns.astype(str)
            df['type'] = df.type.apply(len)

            # splitting the multiple column
            multi_col = df.multipliers.fillna(np.NaN).apply(pd.Series)
            multi_col.columns = 'multiplier_' + multi_col.columns.astype(str)
            df['multipliers'] = df.multipliers.apply(lambda x: len(x) if type(x)==list else 0)

            # splitting the weaknesses column
            weak_col = df.weaknesses.apply(pd.Series)
            weak_col.columns = 'weakness_' + weak_col.columns.astype(str)
            df['weaknesses'] = df.weaknesses.apply(len)

            # splitting the prev_evolution column
            prev_evol = df.prev_evolution.apply(pd.Series)
            df['prev_evolution'] = df.prev_evolution.apply(lambda x: len(x) if type(x)==list else 0)
            # converting dictonary object into different columns
            prev_1 = pd.json_normalize(prev_evol[0])
            prev_1.columns = 'prev_evol_1_' + prev_1.columns.astype(str)
            prev_2 = pd.json_normalize(prev_evol[1])
            prev_2.columns = 'prev_evol_2_' + prev_2.columns.astype(str)

            # splitting the next_evolution column
            next_evol = df.next_evolution.apply(pd.Series)
            df['next_evolution'] = df.next_evolution.apply(lambda x: len(x) if type(x)==list else 0)
            # converting dictonary object into differnt columns
            next_1 = pd.json_normalize(next_evol[0])
            next_1.columns = 'next_evol_1_' + next_1.columns.astype(str)

            next_2 = pd.json_normalize(next_evol[1])
            next_2.columns = 'next_evol_2_' + next_2.columns.astype(str)

            next_3 = pd.json_normalize(next_evol[2])
            next_3.columns = 'next_evol_3_' + next_3.columns.astype(str)
            logging.info('Joining DataFrames')
            # joining the columns into original dataframe
            df = df.join((type_col, multi_col, weak_col, prev_1, prev_2, next_1, next_2, next_3))
            logging.info(f'Saving Excel file at ./{file_name}')
            df.to_excel(file_name, sheet_name='Pokemon_Data', index=False)
        except:
            # Raises ValueError if not able to parse JSON
            logging.error('Failed to Decode Raw Data')
            raise ValueError('Invalid JSON')
    else:
        # Raises RequestError if not able to make https request
        logging.info('Sending Reqest Failed')
        raise exceptions.RequestError(pool=https, url=url, message='Invalid URL!')












if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/Biuni/PokemonGO-Pokedex/master/pokedex.json'
    json_to_excel(url, 'pokemon.xlsx')
