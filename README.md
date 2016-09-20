# 音Tag

This is a music library organization application that lets you apply freeform tags to each track. And then you can find tracks by tag. This application is written as a potential solution to the problem that every lover of non-mainstream music has faced.

Especially written for otakus by an otaku.

Want an idea of how to use this?
Well, suppose you want your music organized into some categories like 'Anime music', 'Anime OSTs', 'Game OSTs', 'Vocaloid', 'Doujin', 'Touhou'.

You could hit some commands like:
~~~~
ontag tag <search criteria for your anime music> anime
ontag tag <search criteria for your anime OSTs> anime ost
ontag tag <search criteria for all your game OSTs> game ost
ontag tag <search criteria for all your vocaloid music> vocaloid
~~~~

Want to find all anime music?
~~~~
ontag list anime
~~~~
But this will give you both the anime music and the anime osts you set earlier.
Want to find anime music that doesn't come under your OSTs? (Only Anime OSTs?)
~~~~
ontag list anime '!ost' # the way to specify an exclusion tag is '!'. I put the tag in single quotes to keep it from being interpreted by the shell
~~~~

Want to list all music that comes under doujin music?
~~~~
ontag subtag doujin vocaloid touhou #just as an example, since much of Vocaloid and Touhou is doujin
ontag list doujin
~~~~

Want all doujin music other than vocaloid?
~~~~
ontag list doujin '!vocaloid'
~~~~

Want to make sure you get vocaloid music even if you search for 'ボーカロイド'?
~~~~
ontag synonym vocaloid ボーカロイド
ontag list ボーカロイド
~~~~

*note: all tag matching is case-insensitive, but metadata search criteria is case-sensitive.*

**\*Currently still in the alpha stage. Don't expect everything to work just yet.\***

Syntax:
~~~~
ontag <command> [options] [args]
ontag --help to display the help page.
~~~~

## Commands:

### add
Adds a file/folder into the database. Without arguments, it'll scan the default folder for files and add them.

Or you could use it as:
~~~~
add [--path='<path to file/folder>'] [optional tags to apply while adding]
~~~~
*Warning: I haven't entirely tested how this thing behaves outside of the folder right above the set Music Library.*

### delete
Deletes a file/folder from the database. Without arguments, it'll clear the whole database.

Possible uses:
~~~~
delete [search-criteria] #check 'list' for search-criteria
~~~~

### list
To search through the database.
~~~~
list [--option="content" to search through file meta data] [--fields="comma-separated list of fields to display"] [tags to include/exclude]
~~~~
Options:
--title
~~~~
--artist
--album
--direct : directory to search in
--fname : filename to search for
--rating: minimum rating to search for
~~~~
### tag
Add tags to an entity

Uses:
~~~~
tag [--option="content" to search through file meta data] [tags to apply]
~~~~

Options:
Same as for 'list'

### play
Builds an M3U playlist with the results of a search and plays it.

### rate
Allows you to set a rating to a track. There's no set scale to it, that's up to you. But it must be an integer.

~~~~
rate [search-criteria as in 'list'] <rating>
~~~~

### config
Opens up the config file in your default text editor.

Stuff you can configure at the moment:
+ **Library path** (LIBPATH): The path to the folder that contains all your music.
+ **Log file locations** (GOODLOG and BADLOG): the two files where all normal behavior and errors are recorded respectively

### synonym
Allows you to add a synonym to a term. Like:
~~~~
synonym <old term> <new terms>
~~~~

So that any searches that match the <new term> will also link to the original and vice versa.
Allows synonyms for tags, like:
~~~~
synonym arrangecover remix
~~~~

### subtag
Allows you to attach a tag as a subtag of another. Basically to create 'is-a' relationships. So if you say:

~~~~
subtag electro glitch-hop
~~~~

then 'glitch-hop' is now under 'electro' and searches for 'electro' will also show results with the 'glitch-hop' tag.

### autotag

This will just simply look through the metadata of each track in the library and add the 'title', 'artist', and 'album' fields into tags. Might make things easier to search later.

## More cool ideas on how to use 音Tag:**
Do this:
~~~~
ontag subtag human reol hanatan kradness [more human vocalists]
~~~~
Want to find all human covers of a certain song?
~~~~
ontag list cover matryoshka human
~~~~

Find it annoying when the same artist goes by different names?
~~~~
ontag synonym "Ginsuke Rin" "Ocelot"
~~~~

## How to install:
+ Clone the repo:
~~~~
git clone https://github.com/mikosama326/ontag.git
~~~~
Or download it as a ZIP or whatever.

+ Navigate into folder where setup.py is

+ Install using setuptools
~~~~
pip install .
~~~~
Or whatever suits your fancy. I highly recommend using virtualenv: [https://virtualenv.pypa.io/en/stable/]

+ You'll install Click (for the CLI), TinyTag (for track metadata reading), TinyDB (for the database), and Colorama (for the color-coded output)

## Some output files you'll see:
+ **musicdb.json** : contains the actual database.
+ **trimurthulu.txt** : the config file.
   - LIBPATH: default path to your music library
   - That's all there is in here for now. Don't worry. I'll add stuff later.
