import json
import sys
import urllib
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


youtube_key = "AIzaSyDK9doqhqTeNpfZVP1adsXc8PuuQhVBuFc"
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_path = xbmc.translatePath(xbmcaddon.Addon(id=addon_id).getAddonInfo('path')).decode('utf-8')+"/"
listings_path = addon_path + "resources/listings/"

xbmcplugin.setContent(addon_handle, 'episodes')
#---------------------------------------------------------------------------------------------------
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
#---------------------------------------------------------------------------------------------------
def addCategory(title, field):
    url = build_url({'contains': 'category', 'field': field, 'title': title})
    li = xbmcgui.ListItem(title, iconImage=addon_path+'resources/img/'+field+'.ico.256x256.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
#---------------------------------------------------------------------------------------------------
def addListing(title, field, thumb):
    url = build_url({'contains': 'listing', 'field': field, 'title': title})
    li = xbmcgui.ListItem(title, iconImage=addon_path+'resources/img/'+thumb)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
#---------------------------------------------------------------------------------------------------
def addPlaylist(title, playlist_id):
    url = build_url({'contains': 'playlist', 'field': 'tbd', 'title': title, 'item_id': playlist_id})
    li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
#---------------------------------------------------------------------------------------------------
def addVideo(title, field, video_id):
    url = build_url({'contains': 'video', 'field': field, 'title': title, 'item_id': video_id})
    thumb = "https://i.ytimg.com/vi/"+video_id+"/hqdefault.jpg"
    li = xbmcgui.ListItem(title, iconImage=thumb)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
#---------------------------------------------------------------------------------------------------
def PlayVideoYouTube(video_id):
    play_url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+video_id
    item = xbmcgui.ListItem(path=play_url)
    xbmcplugin.setResolvedUrl(addon_handle, True, item)
    player = xbmc.Player().play(play_url, item)  
#---------------------------------------------------------------------------------------------------

contains = args.get('contains', None)
if contains is None:
    title = 'Dev boards, apps and devices of the sort'
    addListing(title, 'tech.main', 'tech.ico.256x256.jpg')

    title = 'Fashion shows and beauty pageants'
    addListing(title, 'beauty.main', 'beauty.ico.256x256.jpg')

    title = 'SciFi short films and movie clips'
    addListing(title, 'scifi.main', 'scifi.ico.256x256.jpg')

    title = 'Unique taste in music'
    addListing(title, 'music.main', 'music.ico.256x256.jpg')

    title = 'Random acts of humor and funny'
    addListing(title, 'comedy.main', 'comedy.ico.256x256.jpg')

    xbmcplugin.endOfDirectory(addon_handle)

elif contains[0] == 'category':
    addVideo(args['title'][0], 'youtube', 'UsCzsMb7AWY')
    addPlaylist('Playlist test', 'PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG')
    xbmcplugin.endOfDirectory(addon_handle)
elif contains[0] == 'listing':
    with open(listings_path+args['field'][0]+".json") as json_data:
       data = json.load(json_data)
    for token in data["items"]:
        if token["type"] == 'video':
           addVideo(token['title'], 'youtube', token['item_id'])
        elif token["type"] == 'playlist':
           addPlaylist(token['title'], token['item_id'])
        elif token["type"] == 'listing':
           addListing(token['title'], token['item_id'], token['thumb'])

    xbmcplugin.endOfDirectory(addon_handle)
elif contains[0] == 'playlist':
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?maxResults=25&part=snippet&playlistId='+args['item_id'][0]+'&key='+youtube_key
    f = urllib.urlopen(url)
    data = json.load(f)
    f.close()

    count = len(data["items"])
    for token in data["items"]:
        item_id = token["snippet"]["resourceId"]["videoId"]
        thumb = token["snippet"]["thumbnails"]["high"]["url"]
        label = token["snippet"]["title"].encode('utf-8')
        url = build_url({'contains': 'video', 'field':'youtube', 'title': label, 'item_id': item_id})
        item = xbmcgui.ListItem(label, iconImage=thumb, path=url)
        xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=item)
    xbmcplugin.endOfDirectory(addon_handle)
elif contains[0] == 'video':
    PlayVideoYouTube(args['item_id'][0])



