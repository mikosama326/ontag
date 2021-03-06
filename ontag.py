import click
import os
from readfiles import *

@click.group()
@click.pass_context
def cli(ctx):
    mylyfe = open("trimurthulu.txt","r") #this is the config file.
    ctx.obj = {}
    lines = mylyfe.readlines()
    mylyfe.close()
    for line in lines:
        if line[0] != '#':
            key,value = line.strip().split(':')
            ctx.obj[key.strip()] = value.strip()

#add tracks to the library
@cli.command()
@click.option("--path",required=False,default="",help="directory to add files from")
@click.argument('tags',required=False,nargs=-1)
@click.pass_context
def add(ctx,path,tags):
    """To add a song/folder into the library"""
    badlog = open(ctx.obj['BADLOG'],"w+")
    goodlog = open(ctx.obj['GOODLOG'],"w+")
    if path == "":
        #os.path.walk(str(ctx.obj['LIBPATH']),scanfiles,0)
        addAllTheFiles(str(ctx.obj['LIBPATH']),tags,{'goodlog':goodlog,'badlog':badlog})
    else:
        addAllTheFiles(path,tags,{'goodlog':goodlog,'badlog':badlog})
    badlog.close()
    goodlog.close()

#delete entries from the library
@cli.command()
@click.option('--title',required=False,default=".*",help="song title (file meta info)")
@click.option('--artist',required=False,default=".*",help="song artist (file meta info)")
@click.option('--album',required=False,default=".*",help="song album (file meta info)")
@click.option('--direct',required=False,default=".*",help="directory to look in")
@click.option('--fname',required=False,default=".*",help="file name")
@click.option('--rating',required=False,default=0,help="minimum rating")
@click.option('--fields',required=False,default="name,title,artist,album",help="which fields to display")
@click.argument('tags',required=False,nargs=-1)
@click.pass_context
def delete(ctx,title,artist,album,direct,fname,fields,rating,tags):
    """To remove a file from the library"""
    results = searchByTag(title,artist,album,direct,fname,rating,tags)
    deleteAnEntry(results)

#search through the database
@cli.command()
@click.option('--title',required=False,default=".*",help="song title (file meta info)")
@click.option('--artist',required=False,default=".*",help="song artist (file meta info)")
@click.option('--album',required=False,default=".*",help="song album (file meta info)")
@click.option('--direct',required=False,default=".*",help="directory to look in")
@click.option('--fname',required=False,default=".*",help="file name")
@click.option('--rating',required=False,default=0,help="minimum rating")
@click.option('--fields',required=False,default="name,title,artist,album",help="which fields to display")
@click.argument('tags',required=False,nargs=-1)
@click.pass_context
def list(ctx,title,artist,album,direct,fname,fields,rating,tags):
    """To search for a file in the library"""
    results = searchByTag(title,artist,album,direct,fname,rating,tags)
    printResults(results,fields)

#apply tags to a search query
@cli.command()
@click.option('--title',required=False,default=".*",help="song title (file meta info)")
@click.option('--artist',required=False,default=".*",help="song artist (file meta info)")
@click.option('--album',required=False,default=".*",help="song album (file meta info)")
@click.option('--direct',required=False,default=".*",help="directory to look in")
@click.option('--fname',required=False,default=".*",help="file name")
@click.option('--remove',required=False,default=False,is_flag=True,help="set if you want to remove tags")
@click.argument('addtags',required=False,nargs=-1)
@click.pass_context
def tag(ctx,title,artist,album,direct,fname,remove,addtags):
    """To tag a file in the library. Options support regex."""
    #print "TAGGING"
    badlog = open(ctx.obj['BADLOG'],"w+")
    goodlog = open(ctx.obj['GOODLOG'],"w+")
    #print "OPENED LOG FILE IN TAG"
    tagATrack(title,artist,album,direct,fname,addtags,remove,{'goodlog':goodlog,'badlog':badlog})
    badlog.close()
    goodlog.close()

#play files in a search query
@cli.command()
@click.option('--title',required=False,default=".*",help="song title (file meta info)")
@click.option('--artist',required=False,default=".*",help="song artist (file meta info)")
@click.option('--album',required=False,default=".*",help="song album (file meta info)")
@click.option('--direct',required=False,default=".*",help="directory to look in")
@click.option('--fname',required=False,default=".*",help="file name")
@click.option('--rating',required=False,default=0,help="minimum rating")
@click.argument('tags',required=False,nargs=-1)
@click.pass_context
def play(ctx,title,artist,album,direct,fname,rating,tags):
    """To play a file(or multiple files)"""
    click.launch(buildPlaylist(searchByTag(title,artist,album,direct,fname,rating,tags)))

#set a rating to files in a search query
@cli.command()
@click.option('--title',required=False,default=".*",help="song title (file meta info)")
@click.option('--artist',required=False,default=".*",help="song artist (file meta info)")
@click.option('--album',required=False,default=".*",help="song album (file meta info)")
@click.option('--direct',required=False,default=".*",help="directory to look in")
@click.option('--fname',required=False,default=".*",help="file name")
@click.argument('tags',required=False,nargs=-1)
@click.argument('rating',required=True,nargs=1,default=0)
@click.pass_context
def rate(ctx,title,artist,album,direct,fname,tags,rating):
    """To rate a file in the library"""
    results = searchByTag(title,artist,album,direct,fname,0,tags)
    setrate(results,rating)

#open the config file
@cli.command()
@click.pass_context
def config(ctx):
    """To open the config file."""
    click.launch('trimurthulu.txt')

#mark tags as synonyms
@cli.command()
@click.option('--remove',required=False,default=False,is_flag=True,help="set if you want to remove relationship")
@click.argument('tag',required=True,nargs=1)
@click.argument('synonyms',required=True,nargs=-1)
@click.pass_context
def synonym(ctx,remove,tag,synonyms):
    """To join two tags as synonyms"""
    tagsyn(tag,synonyms,remove)

#mark tags as subtags
@cli.command()
@click.option('--remove',required=False,default=False,is_flag=True,help="set if you want to remove relationship")
@click.argument('tag',required=True,nargs=1)
@click.argument('subtags',required=True,nargs=-1)
@click.pass_context
def subtag(ctx,remove,tag,subtags):
    """To add a tag as the subtag of another"""
    tagsub(tag,subtags,remove)

#autotag based on metadata
#Allow to take a 'rules file'
@cli.command()
@click.pass_context
def autotag(ctx):
    """Automatically tags the files based on track metadata"""
    badlog = open(ctx.obj['BADLOG'],"w+")
    goodlog = open(ctx.obj['GOODLOG'],"w+")
    makeMyLifeEasy({'goodlog':goodlog,'badlog':badlog})
    badlog.close()
    goodlog.close()

@cli.command()
def update():
    """
    **Still under construction.**\n
    This is to help you update the content of files that you might have recently changed in your database.
    """
    print '**Still under construction.**'
    print 'This is to help you update the content of files that you might have recently changed in your database.'

@cli.command()
def similar():
    """
    **Still under construction.**\n
    This is to help you find songs similar to a particular one. I'm not quite sure how you're going to specify the seed song.\n
    But I'll work on that.
    """
    print '**Still under construction.**'
    print "This is to help you find songs similar to a particular one. I'm not quite sure how you're going to specify the seed song. "
    print "But I'll work on that."

if __name__ == '__main__':
    cli(obj={})
