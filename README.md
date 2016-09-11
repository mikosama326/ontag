# 音Tag

This is a music library organization application that lets you apply freeform tags to each track. And then you can find tracks by tag. This application is written as a potential solution to the problem that every lover of non-mainstream music has faced.

Especially written for otakus and by an otaku.

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

Want to find anime music that doesn't come under your OSTs?
~~~~
ontag list anime '!ost'
~~~~

Want to list all music that comes under doujin music?
~~~~
ontag subtag doujin vocaloid touhou
ontag list doujin
~~~~

Want all doujin music other than vocaloid?
~~~~
ontag list doujin '!vocaloid' //I haven't actually tested that this works yet. :P
~~~~

Want to make sure you get vocaloid music even if you search for 'ボーカロイド'?
~~~~
ontag synonym vocaloid ボーカロイド
ontag list ボーカロイド
~~~~

*note: all tag matching is case-insensitive, but metadata search criteria is case-sensitive.*

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
add --path='<path to file/folder>' [optional tags to apply while adding]
~~~~

### delete
Deletes a file/folder from the database. Without arguments, it'll clear the whole database.

Possible uses:
~~~~
delete
delete [query] //I haven't put in the proper search criteria yet.
~~~~

### list
To search through the database.
~~~~
list [--option="content" to search through file meta data] [--fields="comma-separated list of fields to display"] [tags to include/exclude]
~~~~
Options:
~~~~
--title
--artist
--album
--direct : directory to search in
--fname : filename to search for
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
Plays a track or playlist in your default music player. Not working yet. Oops. :P

### rate
Allows you to set a rating to a track, and album, or whatever. Can't search through ratings yet. Oops. :P

~~~~
rate [some query] <rating>
~~~~

### config
Opens up the config file in your default text editor.

Stuff you can configure at the moment:
Library path: The path to the folder that contains all your music.

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

**Extra cool ideas on how to use Ontag:**
~~~~
ontag subtag human reol hanatan kradness
~~~~
Want to find all human covers of a certain song?
~~~~
ontag list cover matryoshka human
~~~~

Find it annoying when the same artist goes by different names?
~~~~
ontag synonym "Ginsuke Rin" "Ocelot"
~~~~
