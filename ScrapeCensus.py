import os
import sys
import time
import requests
import json


import pandas as pd
import requests

usernames = []
API_URL="http://api.censusreporter.org/1.0/data/show/{release}?table_ids={table_ids}&geo_ids={geoids}"

def get_data(tables=None, geoids=None, release='latest'):
    if geoids is None:
        geoids = ['040|01000US']
    elif isinstance(geoids,basestring):
        geoids = [geoids]
    if tables is None:
        tables = ['B01001']
    elif isinstance(tables,basestring):
        tables=[tables]

    url = API_URL.format(table_ids=','.join(tables).upper(), geoids=','.join(geoids), release=release)
    response = requests.get(url,timeout=100.0)
    #print(response.json())    
    return response.json()

def get_dataframe(tables=None, geoids=None, release='latest',geo_names=False,col_names=False,include_moe=False):
    response = get_data(tables=tables,geoids=geoids,release=release)
    print(response)
    frame = pd.DataFrame.from_dict(prep_for_pandas(response['data'],include_moe),orient='index')
    frame = frame[sorted(frame.columns.values)] # data not returned in order
    if geo_names:
        geo = pd.DataFrame.from_dict(response['geography'],orient='index')
        frame.insert(0,'name',geo['name'])
    if col_names:
        d = {}
        for table_id in response['tables']:
            columns = response['tables'][table_id]['columns']
            for column_id in columns:
                d[column_id] = columns[column_id]['name']
        frame = frame.rename(columns=d)
    return frame

def prep_for_pandas(json_data,include_moe=False):
    """Given a dict of dicts as they come from a Census Reporter API call, set it up to be amenable to pandas.DataFrame.from_dict"""
    result = {}
    for geoid, tables in json_data.items():
        flat = {}
        for table,values in tables.items():
            for kind, columns in values.items():
                if kind == 'estimate':
                    flat.update(columns)
                elif kind == 'error' and include_moe:
                    renamed = dict((k+"_moe",v) for k,v in columns.items())
                    flat.update(renamed)
        result[geoid] = flat
    return result


def updateInput():
	f = open("input.txt","w")
	for username in usernames:
		f.write(username + "\n")
	f.close()



if __name__ == '__main__':
    tables = ["B03002","B19013","B15003"]
    f = open ("input.txt","rb+")



    for line in f:
        username = line.strip()
        usernames.append(username);

    f.close()


    while True:
        if (len(usernames) == 0):
            break
        failed = False
        usr = usernames[0].zfill(5)
        try:
            df = get_dataframe(tables=tables, geoids=["86000US%s" %usr])
        except:
            failed = True
        if not failed:
            firstLine = os.path.exists("output.txt")
            with open("output.txt", "a+") as myfile:
                df.to_csv(myfile, header=not firstLine)
                myfile.close()
                #out = r.json()
                #myfile.write(json.dumps(out) + "\n")
            print("successfully got data")
            with open("input_done.txt","a+") as myfile2:
                myfile2.write(usr+"\n")
            del usernames[0]
            updateInput()

            print ("Successfully got zip code: " + usr + " there are %d remaining" %len(usernames))

        else:
			print("ERROR: Something is wrong, moving zip to end of list and continuing")
			time.sleep(1 * 1)
			usernames += [usernames.pop(0)]
			updateInput()
			


