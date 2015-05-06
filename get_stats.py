
# coding: utf-8

# In[118]:

import requests
import time 
import json 
import numpy as np
import datetime


# In[119]:

def timeRequest(url_req):
    try:
        t0 = time.time()
        res = requests.get(url_req,timeout=20) 
        print res.status_code
        t1 = time.time()
        time_seconds = t1-t0
    except:
        return None, np.nan
    return res, time_seconds

#
def createOutlineRow(url,time_sec,res,name):
    dt =  datetime.datetime.now()
    if res:
        if res.status_code == 200:
            d = {"name":name ,"type":"outline","url":url,"time":time_sec,"status_code":res.status_code,"note":"ok","date":str(dt),"tz":"EST"}
        else:
            d = {"name":name, "type":"outline","url":url,"time":time_sec,"status_code":res.status_code,"note":"return error","date":str(dt),"tz":"EST"}
    else:    
        d = {"name":name, "type":"outline","url":url,"time":-1,"status_code":"","note":"uframe request error","date":str(dt),"tz":"EST"}
    return d

#
def createAssetsRow(url,time_sec,res,name):
    dt =  datetime.datetime.now()
    if res:
        if res.status_code == 200:
            data = res.json()
            asset_count = 0
            instrument_count = 0
            hasLatLon = 0
            for row in data:
                if row['@class'] == ".AssetRecord":
                    asset_count+=1
                elif row['@class'] == ".InstrumentAssetRecord":
                    instrument_count+=1
                
                hasLon = False
                hasLat = False
                if "metadata" in row:
                    for el in row["metadata"]:
                        if el['key'] == "Latitude":
                            hasLat = True
                        elif el['key'] == "Longitude":
                            hasLon = True
                    if hasLat and hasLon:
                        hasLatLon +=1
                                
            stats = {"total":len(data),"assets_count":asset_count,"instrument_count":instrument_count,"hasll_count":hasLatLon}
            
            d = {"name":name, "stats":stats, "type":"assets","url":url,"time":time_sec,"status_code":res.status_code,"note":"ok","date":str(dt),"tz":"EST"}
        else:
            d = {"name":name, "stats":{}, "type":"assets","url":url,"time":time_sec,"status_code":res.status_code,"note":"return error","date":str(dt),"tz":"EST"}
    else:    
        d = {"name":name, "stats":{}, "type":"assets","url":url,"time":-1,"status_code":"","note":"uframe request error","date":str(dt),"tz":"EST"}
    return d


# In[120]:

def get_info():
    base_url = ["http://uframe.ooi.rutgers.edu:12576/sensor/inv",
                "http://uframe.ooi.rutgers.edu:12576/sensor/inv/toc",   
                "http://uframe.ooi.rutgers.edu:12576/sensor/inv/CP05MOAS/GL001/03-CTDGVM000/metadata",
                "http://uframe.ooi.rutgers.edu:12576/sensor/inv/CP05MOAS/GL001/03-CTDGVM000/telemetered/ctdgv_m_glider_instrument?beginDT=2014-10-06T23:58:44.162Z&endDT=2014-10-07T23:58:44.162Z",                
                ]
    
    base_url_names = ["UFRAME:Inventory",
                      "UFRAME:TOC",
                      "UFRAME:Metadata",
                      "UFRAME:Data 24h - GL004",
                      ]
    
    assets_url = ["http://uframe.ooi.rutgers.edu:12573/assets"]
    
    assets_url_names = ["UFRAME:Assets"]
    
    data_url = []
    
    data_store = {"outline":[],"assets":[]}
    
    #GENERAL OUTLINE
    for i,link in enumerate(base_url):        
        url_req = link
        print url_req
        name = base_url_names[i]
        res, time_seconds = timeRequest(url_req)
        data_store["outline"].append(createOutlineRow(url_req,time_seconds,res,name))        
    
    #ASSETS OUTLINE
    for i,link in enumerate(assets_url):
        url_req = link
        print url_req
        name = assets_url_names[i]
        res, time_seconds = timeRequest(url_req)
        data_store["assets"].append(createAssetsRow(url_req,time_seconds,res,name))
        
    return data_store


# In[121]:

data_store = get_info()


# In[122]:

dt =  datetime.datetime.now()
file_name = "./webcontent/files/ooi_status_"+ str(dt)+".json"
print file_name

with open(file_name, 'w') as outfile:
    json.dump(data_store, outfile, indent=2)

outline_file_name = "./webcontent/files/current.json"
outline_dict = [file_name]
with open(outline_file_name, 'w') as outfile:
    json.dump(outline_dict, outfile, indent=2)
    

with open('./webcontent/files/outline.json') as data_file:    
    data = json.load(data_file)
        
data.append(file_name)    

outline_file_name = "./webcontent/files/outline.json"
outline_dict = data
with open(outline_file_name, 'w') as outfile:
    json.dump(outline_dict, outfile, indent=2)


# In[122]:



