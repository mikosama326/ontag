import click
import os
from readfiles import *

# Warning! This is a repeat declaration. We need to eventually read this data from a file.
#library_path = './testLib'
@click.group()
@click.pass_context
def cli(ctx):
    mylyfe = open("trimurthulu.txt","r")
    ctx.obj = {}
    lines = mylyfe.readlines()
    mylyfe.close()
    for line in lines:
        if line[0] != '#':
            key,value = line.strip().split(':')
            ctx.obj[key] = value

@cli.command()
@click.option("--path",required=False,default="",help="directory to add files from")
@click.argument('tags',required=False,nargs=-1)
#apply tags while adding the tracks to the library
@click.pass_context
def add(ctx,path,tags):
    """To add a song/folder into the library"""
    #print 'To add a song/folder into the library'
    if path == "":
        #os.path.walk(str(ctx.obj['LIBPATH']),scanfiles,0)
        addAllTheFiles(str(ctx.obj['LIBPATH']),tags)
    else:
        addAllTheFiles(path,tags)

@cli.command()
@click.argument('query', default="",required=False,nargs=1)
def delete(query):
    """To remove a file from the library"""
    #print 'To remove a file from the library'
    deleteAnEntry(query)

@cli.command()
@click.option('--title',required=False,default=".*",help="song title (file meta info)")
@click.option('--artist',required=False,default=".*",help="song artist (file meta info)")
@click.option('--album',required=False,default=".*",help="song album (file meta info)")
@click.option('--direct',required=False,default=".*",help="directory to look in")
@click.option('--fname',required=False,default=".*",help="file name")
@click.option('--rating',required=False,default=0,help="minimum rating")
@click.option('--fields',required=False,default="name,title,artist,album",help="which fields to display")
#add search by rating
@click.argument('tags',required=False,nargs=-1)
def list(title,artist,album,direct,fname,fields,rating,tags):
    """To search for a file in the library"""
    #print 'To search for a file in the library'
    #listtracks(query,fields)
    searchByTag(title,artist,album,direct,fname,rating,fields,tags)

@cli.command()
@click.option('--title',required=False,default=".*",help="song title (file meta info)")
@click.option('--artist',required=False,default=".*",help="song artist (file meta info)")
@click.option('--album',required=False,default=".*",help="song album (file meta info)")
@click.option('--direct',required=False,default=".*",help="directory to look in")
@click.option('--fname',required=False,default=".*",help="file name")
#@click.argument('query', default="",required=False,nargs=1)
@click.argument('tags',required=True,nargs=-1)
#remove option
def tag(title,artist,album,direct,fname,tags):
    """To tag a file in the library. Options support regex."""
    #print 'To tag a file in the library.'
    tagATrack(title,artist,album,direct,fname,tags)

@cli.command()
def play():
    """To play a file(or multiple files)"""
    print 'To play a file(or multiple files) from the library'

@cli.command()
@click.argument('query',required=True,nargs=1)
@click.argument('rating',required=True,nargs=1,default=0)
def rate(query,rating):
    """To rate a file in the library"""
    #print 'To rate a file in the library'
    setrate(query,rating)

@cli.command()
def config():
    """To open the config file."""
    print 'To open the config file.'
    os.system('trimurthulu.txt')
    #yays = open("trimurthulu.txt","r+")
    #yays.write("LIBPATH: ./testLib\n")

@cli.command()
@click.argument('tag',required=True,nargs=1)
@click.argument('synonyms',required=True,nargs=-1)
#delete option
def synonym(tag,synonyms):
    """To join two tags as synonyms"""
    #print 'To join two tags as synonyms'
    tagsyn(tag,synonyms)

@cli.command()
@click.argument('tag',required=True,nargs=1)
@click.argument('subtags',required=True,nargs=-1)
#delete option
def subtag(tag,subtags):
    """To add a tag as the subtag of another"""
    #print 'To add a tag as the subtag of another'
    tagsub(tag,subtags)

@cli.command()
def autotag():
    """Automatically tags the files based on the ID3 information"""
    makeMyLifeEasy()

if __name__ == '__main__':
    cli(obj={})
