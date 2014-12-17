# -*- coding: utf-8 -*-

"""
Version 1.0.1 (2014.07.04)
- initial release
"""

import urllib
import urllib2
import json
import time
import hashlib
import uuid
import re
import random



class Client:
    def __init__(self, config):
        self.Config = config
        
    def _calculateToken(self, timestamp, params={}):
        token = ""
        
        hashmap = {}
        hashmap.update(params)
        
        stringbuilder = ""
        stringbuilder += self.Config.get('key_tablet', '')
        stringbuilder += ";"
        stringbuilder += self.Config.get('salt_tablet', '')
        stringbuilder += ";"
        stringbuilder += timestamp
        
        params = sorted(hashmap.items())
        
        for param in params:
            stringbuilder += ";"
            stringbuilder += param[1]
        
        if len(hashmap)==0:
            stringbuilder += ";"
           
        try:
            messagedigest = hashlib.md5()
            messagedigest.update(stringbuilder);
            abyte0 = messagedigest.digest();
            length = len(abyte0);
            
            for b in bytearray(abyte0):
                val = b
                val = 0x100 | 0xFF & val
                hval = hex(val).lower()
                token += hval[3:]
        except:
            token = ""
            
        return token
        
    def _createQueryArgs(self, params={}):
        result = {}
        result.update(params)
        
        result['_key'] = self.Config.get('key_tablet', '')
        timestamp = str(int(time.time()))
        result['_ts'] = timestamp
        result['_tk'] = self._calculateToken(timestamp, params)
        result['_auth'] = 'integrity'
        
        return result
        
    def _createRequest(self, url_path, params={}):
        if not url_path.startswith(self.Config.get('url', '')):
            url = self.Config.get('url', '')
            if not url.endswith('/') and not url_path.startswith('/'):
                url+='/'
            url = url+url_path

        request = urllib2.Request(url)
        
        # always set the id
        params['id'] = self.Config.get('id', '0')
        
        # prepare header
        header = self.Config.get('http-header', {})
        for key in header:
            request.add_header(key, header.get(key, ''))
            
        # calculate token and set params
        query_args = self._createQueryArgs(params)
        request.add_data(urllib.urlencode(query_args))
        return request
                               
    def _request(self, url_path, params={}):
        request = self._createRequest(url_path, params)
        
        result = {}
        try:
            content = urllib2.urlopen(request)
            result = json.load(content, encoding='utf-8')
            success = result.get('success', False)
            if success==True:
                result = result.get('result', {})
        except:
            # do nothing
            pass
        
        return result

    
    def getEpisodeDetails(self, id):
        params = {'filmid': id}
        return self._request('/api/query/json/content.film_details', params)
    
    def getEpisodeVideoUrl(self, id):
        finalUrl = None
        film = self.getEpisodeDetails(id)
        film = film.get('content', {})
        film = film.get('film', {})
        videoUrl = film.get('videourl', None)
        if videoUrl!=None:
            """
            This is part an implementation of rtl_now provided by AddonScriptorDE
            """
            opener = urllib2.build_opener()
            userAgent = "Mozilla/5.0 (Windows NT 5.1; rv:24.0) Gecko/20100101 Firefox/24.0"
            opener.addheaders = [('User-Agent', userAgent)]
            content = opener.open(videoUrl).read()
            match = re.compile("data:'(.+?)'", re.DOTALL).findall(content)
            hosterURL = videoUrl[videoUrl.find("//")+2:]
            hosterURL = hosterURL[:hosterURL.find("/")]
            url = "http://"+hosterURL+urllib.unquote(match[0])
            content = opener.open(url).read()
            match = re.compile('<filename.+?><(.+?)>', re.DOTALL).findall(content)
            url = match[0].replace("![CDATA[", "")
            matchRTMPE = re.compile('rtmpe://(.+?)/(.+?)/(.+?)]', re.DOTALL).findall(url)
            matchHDS = re.compile('http://(.+?)/(.+?)/(.+?)/(.+?)/(.+?)\\?', re.DOTALL).findall(url)
            if matchRTMPE:
                playpath = matchRTMPE[0][2]
                if ".flv" in playpath:
                    playpath = playpath[:playpath.rfind('.')]
                else:
                    playpath = "mp4:"+playpath
                finalUrl = "rtmpe://"+matchRTMPE[0][0]+"/"+matchRTMPE[0][1]+"/ playpath="+playpath+" swfVfy=1 swfUrl=http://"+hosterURL+"/includes/vodplayer.swf app="+matchRTMPE[0][1]+"/_definst_ tcUrl=rtmpe://"+matchRTMPE[0][0]+"/"+matchRTMPE[0][1]+"/ pageUrl="+videoUrl
            elif matchHDS:
                finalUrl = "rtmpe://fms-fra"+str(random.randint(1, 34))+".rtl.de/"+matchHDS[0][2]+"/ playpath=mp4:"+matchHDS[0][4].replace(".f4m", "")+" swfVfy=1 swfUrl=http://"+hosterURL+"/includes/vodplayer.swf app="+matchHDS[0][2]+"/_definst_ tcUrl=rtmpe://fms-fra"+str(random.randint(1, 34))+".rtl.de/"+matchHDS[0][2]+"/ pageUrl="+videoUrl
                
        return finalUrl