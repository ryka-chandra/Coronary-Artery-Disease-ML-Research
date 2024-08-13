
# coding: utf-8

home_dir ="/remote/hamedn/Summer2018"

'''All of Tims import statements'''
import random
import numpy as np
# import scipy as sp
# from numpy import linalg as LA
import matplotlib
import matplotlib.pyplot as plt
# import statsmodels.formula.api as smf
import pandas as pd
# import pyodbc
# import glob
import datetime
import glob
import seaborn as sns
sns.set_style("whitegrid")
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score
import itertools
from math import log
pd.options.display.max_rows = 1000
all_groups = map("".join, list(itertools.product('0123456789abcdef', repeat=2)))
import argparse
import json
import pprint
import sys
import urllib


# In[3]:


# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
#from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 1


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info '         'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


# In[26]:


maxResults = 2000
term = ""


def getZipcodeData(zipcode,radius):
    logfile = open(home_dir+"/log.txt","a+")
    location = str(zipcode).zfill(5)
    
    with open(home_dir + "/exports/%s.txt" %location, "w") as myfile:
        for cat in ["homeservices"]:
            for i in range(0,int(1000/50)):
                url_params = {
                            'term': term.replace(' ', '+'),
                            'location': location.replace(' ', '+'),
                            'limit':50,
                            'sort_by':'distance',
                            'offset':(i*50),
                            'radius': radius, # max 40k
                            'categories': cat, #"active", "fitness" , "hotdogs" for fast food
                        }
                temp = request(API_HOST,  SEARCH_PATH, api_key=API_KEY, url_params=url_params)
                
                data = {"request":url_params,"response":temp}
                myfile.write(json.dumps(data)+"\n")  
                logfile.write(str((i,cat)) + "\n")
                #print(url_params)
                #print((i,cat))
                
                if (len(temp["businesses"])==0):
                    break
    print("completed zipcode: " + str(zipcode))
    logfile.write("completed zipcode: " + str(zipcode) + "\n")
    logfile.close()


# In[21]:


def updateInput():
    f = open (home_dir+"/input.csv","w")
    for line in zipcodes:
        f.write(line + "\n")
    f.close()


# In[ ]:


f = open (home_dir+"/input.csv","rb+")
zipcodes = []
for line in f:
    zipcode = line.strip().decode("utf-8")
    zipcodes.append(zipcode);
f.close()


while True:
    if (len(zipcodes) == 0):
        break
    getZip = zipcodes[0].split(",")
    zzz = getZip[0].strip()
    zzz2 = int(getZip[1].strip())
        
    getZipcodeData(zzz2,zzz)
    ap = zipcodes.pop(0)
    updateInput()
    with open(home_dir + "/done.txt", "a") as myfile:
        myfile.write("\n" + ap)
        myfile.close()

