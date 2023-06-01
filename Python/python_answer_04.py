
##############################
###### Python Answer 4 #######
##############################

# A program to download the data from the link and then read the data and convert the into
# the proper structure and return it as a CSV file.





##############################
########## Solution ##########
##############################

# importing urllib3 library for making https requests
# json5 for converting json into dictionary
# csv for writing data into csv format

from urllib3 import PoolManager, exceptions
import csv, json5



def json_to_csv(url: str, file_name: str) -> None:
    '''Download json data from url and write data to given file_name after convert json in csv.'''

    https = PoolManager()

    # sending https request to given url
    response = https.request('GET', url)

    # checking the response
    if response.status == 200:
        try:
            # loading the json data into python dictionary
            data = json5.loads(response.data)

            # formating the data
            for item in data:
                item['reclat'] = item.get('reclat')
                item['reclong'] = item.get('reclong')
                item['geoloc_type'] = item.get('geolocation', {'type':None})['type']
                item['geoloc_coordinate_long'], item['geoloc_coordinate_lat'] = item.get('geolocation', {'coordinates':[None, None]})['coordinates']
                item['year'] = item.get('year', '')[:4]
                item.pop(':@computed_region_cbhk_fwbd', None)
                item.pop(':@computed_region_nnqa_25f4', None)
                item.pop('geolocation', None)
            
            # Opening a file in write mode
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                # setting the header of csv to keys of dictionary
                column_names = data[0].keys()

                # initializing the DictWriter Class
                writer = csv.DictWriter(csvfile, fieldnames=column_names)
                
                # writing the header of csv
                writer.writeheader()

                # writing the rows to csv
                writer.writerows(data)
        except:
            # Raises ValueError if not able to parse JSON
            raise ValueError('Invalid JSON')
    
    else:
        # Raises RequestError if not able to make https request
        raise exceptions.RequestError(pool=https, url=url, message='Invalid URL!')




if __name__ == '__main__':

    url = 'https://data.nasa.gov/resource/y77d-th95.json'
    json_to_csv(url, 'Meteorite_data.csv')