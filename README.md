# 音Tag *(OnTag)*

This is a music library organization application that lets you apply freeform tags to each track. And then you can find tracks by tag. This application is written as a potential solution to the problem that every lover of non-mainstream music has faced.

Especially written for otakus by an otaku.

## What's so great about this?

Well, maybe nothing.

But I love music. And I love organizing things. And like most people who have a widely varied music collection, I have been faced with the connundrum of trying to have some semblance of order in my music collection. And it looks like I'm not alone in the specific situation I'm in; clearly this guy had it rough, too: [http://blog.pkh.me/p/15-the-music-classifying-nightmare.html]

I know bro. I feel you.

So after thinking, thinking and thinking some more, this is the solution I have come up with:

**Step 1:** Stop using this 'artist:someartist', 'album:somealbum', 'genre:somegenre' nonsense. It's not flexible enough for the kinds of music I deal with. I mean, who's the 'artist' for a vocaloid song cover composed by 八王子P originally sung by Hatsune Miku and then covered by 花たん? (I don't know any such songs, actually. This needs to be a thing.) Instead, switch to freeform text without any fields. What I mean is, mark this hypothetical song as '八王子' '花たん' 'cover'. Done. (You'll see why we don't need 'hatsune miku' later. Though you can put it if you want.)

**Step 2:** Define synonyms. Why? You know what's a huge pain? When some songs are marked '初音ミク' and others are marked 'Hatsune Miku' and now you need to make two separate searches. The solution? Mark those two as synonyms of each other. Do this for all such situations where two terms mean the same thing ('same-as' relationships). You can also do it for more itty bitty situations like '八王子' same-as '八王子P'.

**Step 3:** Hierarchy. Organize your tags into a tree using 'is-a' relationships. For example, 'Hatsune Miku' 'is-a' 'Vocaloid'. So is 'Kagamine Rin'. Similarly, '花たん' is-a 'human'. I mean, her voice is godly. But that's besides the point. This is especially helpful for dealing with sub-genres. Yeah, I know. You're welcome.

Ta da!! Now you can search for things like:
*'八王子' 'original'*
to get all original songs by 八王子P.
Or try something like:
*'八王子' 'utau' 'cover'*
to get all UTAU covers of songs by 八王子.
Want remixes of music from Puella Magi Madoka Magika? Try *'madoka magika' 'remix'*.

And so I have written this application, 音Tag, to do all this for you. Plus some extra cute stuff. For now, you'll have to create most of the tags and their relationships manually. But it's not that hard. Ganbare!

## More use ideas (skip this if you're bored already)

Okay, let's try this with some syntax.
Suppose you want your music organized into some categories like 'Anime music', 'Anime OSTs', 'Game OSTs', 'Vocaloid', 'Doujin', 'Touhou'.

You could hit some commands like:
~~~~
ontag tag <search criteria for your anime music> anime
ontag tag <search criteria for your anime OSTs> anime ost
ontag tag <search criteria for all your game OSTs> game ost
ontag tag <search criteria for all your vocaloid music> vocaloid
~~~~
*we'll work on the syntax for the search criteria later*

Want to find all anime music?
~~~~
ontag list anime
~~~~
But this will give you both the anime music and the anime osts you set earlier.
Want to find anime music that doesn't come under your OSTs?
~~~~
ontag list anime '!ost'
~~~~
*the way to specify an exclusion tag is '!'. I put the tag in single quotes to keep it from being interpreted by the unix shell*

Want to list all music that comes under doujin music?
~~~~
ontag subtag doujin vocaloid touhou
ontag list doujin
~~~~
*just as an example, since much of Vocaloid and Touhou is doujin. I realize that there is non-doujin vocaloid music.*

Want all doujin music other than vocaloid?
~~~~
ontag list doujin '!vocaloid'
~~~~

Want to make sure you get vocaloid music even if you search for 'ボーカロイド'?
~~~~
ontag synonym vocaloid ボーカロイド
ontag list ボーカロイド
~~~~

*note: all tag matching is case-insensitive, but metadata search criteria is case-sensitive. Watch out.*

Try this:
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

Assign a language to each song.
~~~
ontag tag --direct="Japanese" japanese
ontag synonym japanese 日本語
~~~

**\*Currently still in the alpha stage. Don't expect everything to work just yet.*** <br />
*please don't kill me*

Okay so the actual syntax:
~~~~
ontag <command> [options] [args]
ontag --help to display the help page.
~~~~
Now what is this elusive **'search-criteria'** you see everywhere? Here you go: <br />
*[--option="content" to search through file meta data]* When using multiple, they are ANDed.
Options:
~~~~
--title : title metadata
--artist : artist metadata
--album : album metadata
--genre : genre metadata
--direct : directory to search in (actually does a partial match by default, instead of a perfect match)
--fname : filename to search for
--rating: minimum rating to search for
~~~~
*--rating doesn't work yet. Don't try it.* <br />
*Oh, and you can use regular expressions in these.*

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
delete [search-criteria]
~~~~
*check 'list' for search-criteria*

### list
To search through the database.
~~~~
list [search-criteria] [--fields="comma-separated list of fields to display"] [tags to include/exclude]
~~~~

Options (aka the "search-criteria" you see everywhere else):
~~~~
--title
--artist
--album
--genre
--direct : directory to search in
--fname : filename to search for
--rating: minimum rating to search for
~~~~
*--rating doesn't work yet. Don't try it.*

### tag
Add tags to an entity

Uses:
~~~~
tag [search-criteria] [tags to apply]
~~~~

--remove to remove the tags instead of applying them

### play
Builds an M3U playlist with the results of a search and plays it.

Not much else right now. Check the TODO.md file to see some of the stuff it's supposed to be able to do.

### rate
Allows you to set a rating to a track. There's no set scale to it, that's up to you. But it must be an integer.

~~~~
rate [search-criteria] <rating>
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
   - GOODLOG: log file where normal log info is stored
   - BADLOG: log file where errors are stored
   - IGNORE: folders to ignore while adding into the library
