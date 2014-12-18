import urlparse


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


url_comps = urlparse.urlparse('http://rtl-now.rtl.de/rtl-aktuell/thema-ua-erbschaftssteuer.php?film_id=183085&player=1&season=0')
url = '%s://%s/%s' % (url_comps.scheme, url_comps.hostname, url_comps.path)
query = dict(urlparse.parse_qsl(url_comps.query))
x=0