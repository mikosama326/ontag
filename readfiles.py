from tinydb import TinyDB, Query
from tinytag import TinyTag
import os
from hashing import *
from utilities import *
#import sys

# WARNING : it is a HUGE mess in here. Proceed at your own risk.

# some global variables we'll need
#library_path = './testLib' # Path to the music library we'll be working on
musicdb = 'musicdb.json' # Path to the database file used to store the database for our library
supported_formats = ['.mp3','.wav','.ogg','.flac','wma','.m4a']
# Okay, first we open up our database
MusicDB = TinyDB(musicdb)
#Artists = MusicDB.table('Artists')
#Genres = MusicDB.table('Genres')
SynTags = MusicDB.table('SynTags')
SubTags = MusicDB.table('SubTags')
Tags = MusicDB.table('Tags')
TagLinks = MusicDB.table('TagLinks')
#Albums = MusicDB.table('Albums')
Q = Query() #makes life easier. I hope.

#To add all the files into the database and apply some tags while adding them
def addAllTheFiles(root,tags):
    files = [ os.path.join(root,f) for f in os.listdir(root) if os.path.isfile(os.path.join(root,f))]
    dirs = [ d for d in os.listdir(root) if os.path.isdir(os.path.join(root,d))]
    #print "=====FILES====="
    #print files
    #print "=====DIRS====="
    #print dirs
    #print "=====ROOT====="
    #print root
    for d in dirs:
        print "---" + d
        files_in_d = addAllTheFiles(os.path.join(root,d),tags)
        #print "=========FILES_IN_D========="
        #print files_in_d
        if files_in_d:
            for f in files_in_d:
                if os.path.exists(f):
                    #print "++",f
                    files.append(os.path.join(root,f))
                    filename, file_extension = os.path.splitext(f.split('/')[-1])
                    if file_extension in supported_formats:
                        #stats = os.stat(f)
                        #cools = True
                        yays = hashMyFileMD5(f)
                        try:
                            tag = TinyTag.get(f)
                        except Exception as oops:
                            print "Oops, looks like we couldn't read the metadata of this file: "+f
                            print oops
                            print "Adding without metadata + " + yays + " " + filename
                            cools = False
                            MusicDB.insert({'id' : yays, 'path' : f[2:], 'name' : filename, 'format' : file_extension[1:], 'tags' : list(tags), 'rating' : 0, 'artist' : "", 'album' : "", 'title' : "", 'genre' : "" })
                            continue
                        #if cools:
                        if MusicDB.contains(Q.id == yays):
                            print "<-> " + yays + " " + filename + " already exists in here. Or there's a hash collision. You're screwed."
                        else:
                            print "Adding + " + yays + " " + filename
                            MusicDB.insert({'id' : yays, 'path' : f[2:], 'name' : filename, 'format' : file_extension[1:], 'tags' : list(tags), 'rating' : 0, 'artist' : tag.artist if tag.artist is not None else "", 'album' : tag.album if tag.album is not None else "", 'title' : tag.title if tag.title is not None else "", 'genre' : tag.genre if tag.genre is not None else "" })
    return files

def makeMyLifeEasy(): # for autotagging
    results = MusicDB.search(Q.name.matches(""));
    for result in results:
        try:
            info = TinyTag.get(result['path']);
        except Exception as oops:
            print "Oops, looks like we couldn't read the metadata of this file: "+f
            print oops
            print "So not autotagging this file."
            return
        if info.title is not None:
            if info.title not in result['tags']:
                result['tags'].append(info.title.lower())
        if info.album is not None:
            if info.album not in result['tags']:
                result['tags'].append(info.album.lower())
        if info.artist is not None:
            if info.artist not in result['tags']:
                result['tags'].append(info.artist.lower())
        if info.genre is not None:
            if info.genre not in result['tags']:
                result['tags'].append(info.genre.lower())
        MusicDB.update({'tags':result['tags']},Q.id == result['id'])
        print result['name'],"-",StringAList(result['tags'])
    print "You're welcome. :)"

def getSynonyms(tag):
    synonyms = [tag]
    synresults = SynTags.search(Q.tag.matches(tag))
    if synresults == []:
        return synonyms
    for synresult in synresults:
        synonyms.append(synresult['synonym'])
    for synonym in synonyms:
        if synonym not in synonyms:
            synonyms += getSynonyms(synonym)
    return list(set(synonyms))

def getSubtags(tag):
    sub = [tag]
    subresults = SubTags.search(Q.tag.matches(tag))
    if subresults == []:
        return sub
    for subresult in subresults:
        sub.append(subresult['subtag'])
    for s in sub:
        if s not in sub:
            sub += getSubtags(s)
    return list(set(sub))

def toInclude(tag):
    if tag[0] == '!':
        return False
    else:
        return True

def isThisInHere(this,here):
    common = list(set(this).intersection(here))
    if common == []:
        return False
    else:
        return True

#omigawd such a bad design. what to do. -_\(0_0)/_-
def searchByTag(title,artist,album,direct,fname,rating,fields,tags):
    results = MusicDB.search(Q.title.matches(title) & Q.artist.matches(artist) & Q.album.matches(album) & Q.path.matches(".*"+direct+".*") & Q.name.matches(".*"+fname+".*"));
    tags = list(tags)
    fields = fields.split(",")
    didWeFindAny = False # just to check if we found even one
    for result in results:
        #print "Checking this one:",result['title']
        flag = True
        for tag in tags:
            tag = tag.lower()
            yay = toInclude(tag) #holds whether we want this tag to be included
            if not yay: #if we're supposed to exclude this tag, remove the '!'
                tag = tag[1:]
            subtags = getSubtags(tag)# first get all the subtags
            synonyms = []
            for subtag in subtags:
                synonyms += getSynonyms(subtag)
            synonyms = list(set(synonyms))

            if isThisInHere(result['tags'],synonyms) != yay:
                flag = False
                break
        if flag:
            didWeFindAny = True
            print formatTheseFields(result,fields)
    if not didWeFindAny:
        print "Oops, no results matching your query."

def tagATrack(title,artist,album,direct,fname,tags,toRemove):
    results = MusicDB.search(Q.title.matches(title) & Q.artist.matches(artist) & Q.album.matches(album) & Q.path.matches(".*"+direct+".*") & Q.name.matches(".*"+fname+".*"));
    if results == []:
        print "Oops no tracks matching your query."
        return
    tags = list(tags)
    for tag in tags:
        tag = tag.lower()
    for result in results:
        if not toRemove:
            result['tags'] = result['tags'] + tags
        else:
            result['tags'] = [item for item in result['tags'] if item not in tags]
        result['tags'] = list(set(result['tags']))
        MusicDB.update({'tags':result['tags']},Q.id == result['id'])
        print result['name'],"-",StringAList(result['tags'])

def deleteAnEntry(query):
    results = MusicDB.search(Q.name.matches(query))
    for result in results:
        print result['name']
    ans = raw_input("You're about to delete all these entries from the database. Are you okay with that?\n")
    while ans not in ['y','yes','no','n']:
        ans = raw_input("Possible answers: 'y', 'yes','n','no'")
    if ans in ['y','yes']:
        MusicDB.remove(Q.name.matches(query))
        print 'deleting complete'
    elif ans in ['n','no']:
        print 'Okay, not deleting.'

def tagsyn(tag,synonyms):
    synonyms = list(synonyms)
    tag = tag.lower()
    for synonym in synonyms:
        synonym = synonym.lower()
        if SynTags.contains(Q.tag.matches(tag) & Q.synonym.matches(synonym)):
            print tag,"<=>",synonym,"combination already exists."
        else:
            SynTags.insert({'tag':tag,'synonym':synonym})
            SynTags.insert({'tag':synonym,'synonym':tag})
            print "Inserted",synonym,"as synonym to",tag

def tagsub(tag,subtags):
    subtags = list(subtags)
    tag = tag.lower()
    for subtag in subtags:
        subtag = subtag.lower()
        if SubTags.contains(Q.tag.matches(tag) & Q.subtag.matches(subtag)):
            print tag,"->",subtag,"relationship already exists."
        else:
            SubTags.insert({'tag':tag,'subtag':subtag})
            print "Inserted",subtag,"as subtag to",tag

def setrate(query,rate):
    results = MusicDB.search(Q.name.matches(query));
    for result in results:
        MusicDB.update({'rating':rate},Q.id == result['id'])
        print "Changed rating of",result['title'],"to",rate

def buildPlaylist(results):
    FORMAT_DESCRIPTOR = "#EXTM3U"
    RECORD_MARKER = "#EXTINF"
    TEMP_PLAYLIST_FILE = "myplaylist.m3u"
    myplaylist = FORMAT_DESCRIPTOR + "\n"
    for result in results:
        try:
            tag = TinyTag.get(result['path'])
        except Exception as oops:
            print "Oops, looks like we couldn't read the metadata of this file: "+f
            print oops
            print "So we can't add this to the playlist. Sorry. :("

        line1 = RECORD_MARKER + ":" + tag.duration + "," + result['title'] if result['title'] is not "" else result['name'] + "\n"
        line2 = result['path'] + "\n"
        totalentry = line1 + line2 + "\n"
        myplaylist = myplaylist + totalentry
    play = open(TEMP_PLAYLIST_FILE,"r+")
    play.write(myplaylist)
    play.close()
    return TEMP_PLAYLIST_FILE
