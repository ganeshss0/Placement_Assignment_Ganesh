
##############################
###### Python Answer 5 #######
##############################

# A program to download the data from the API link and then extract the following data with
# proper formatting.



##############################
########## Solution ##########
##############################



# importing urllib3 library for making https requests
# json5 for converting json into dictionary
# csv for writing data into csv format

from urllib3 import PoolManager, exceptions
import csv, json5
import re, time



def API_to_csv(url: str, file_name: str = 'data.csv') -> None:
    '''Download json data from url and write data to given file_name after convert json in csv.'''

    https = PoolManager()

    # sending https request to given url
    response = https.request('GET', url)

    # checking the response
    if response.status == 200:
        try:
            # loading the json data into python dictionary
            data = json5.loads(response.data)
            data = data['_embedded']['episodes']

            # formating the data
            for item in data:
                # converting 24 hour time to 12 hour time
                item['airtime'] = time.strftime('%I:%M %p', time.strptime(item['airtime'], '%H:%M'))
                item['average_rating'] = item['rating']['average']

                # removing the paragraph tag from string
                item['summary'] = re.findall('<p>(.+)</p>', item['summary'])[0]
                item['medium_image'] = item['image']['medium']
                item['original_image'] = item['image']['original']

                # removing keys that are not using
                item.pop('airstamp'), item.pop('rating')
                item.pop('image'), item.pop('_links')
            
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

    url = 'http://api.tvmaze.com/singlesearch/shows?q=westworld&embed=episodes'
    API_to_csv(url)