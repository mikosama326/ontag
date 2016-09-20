# A To-do list for OnTag

*This is just a place to dump ideas. Don't take it too seriously.*

+ Come up with a name for this
+ Adding tags as a 'set' in each entry
+ Reading ID3 tags and allowing you to add them as tags
  + Create a wrapper that allows you to browse existing ID3 tags
+ A system to create commands, or an in-terminal process?
+ How the heck do you use multiple files to separate functions?
+ A way to traverse and search without opening up the json file. Basically, wrap the TinyDB functions.
x Actually using hashtags with #tag syntax. It'll look cool.
+ Make it work on non-unix filesystems
x Create tables for Tracks, Albums, Artists, Genres
+ Synonym field for the database
x Do we need to write meta tags as well? I don't think it'll be required... 逆になんか面倒くさい.
- Create an application that just runs each command one after the other.
- Create a new database schema that makes searches and inserts faster
- Actually do some hash-y stuff that gives the hashtags its name
- Fix those hash collisions. What the hell.
- Fix the recursive walk function. It's doing some funky stuff.

!!

- Or actually, I think I'll use Click instead. [https://www.youtube.com/watch?v=kNke39OZ2k0]

# Possible commands and syntax

## add
Adds a file/folder into the database. Without arguments, it'll scan the default folder for files and add them.

Or you could use it as:
add --path="<path to folder to add>" [tags to apply]

## delete
Deletes a file/folder from the database. Without arguments, it'll clear the whole database.

Possible uses:
delete
delete <search-criteria>

## list
To search through the database. Short-form as ls.

list <search-criteria>

Possible uses:
list [--artist=""] [--album=""] [--title=""] [--fname=""] [--direct=""] [--fields=""] [--rating=N] [tags]

**I'd like to see if we can color-code the output to make it legible.**
**Also, some regex in there might be nice.**

## tag
Add hashtags to an entity

Uses:
tag <search-criteria> tag1 tag2 ...
<search-criteria> works the same as the ones in list.
--remove: remove a tag

## play
Plays a track or playlist in your default music player.

Use:
play <search-criteria>
play -n<no.of Tracks=k> //picks up the first 'k' tracks that match the criteria
play -r -n k //randomly selects 'k' tracks from your library
play --recently-played //selects the most recent plays from your library
play --recently-added //selects the most recently added tracks

--fname : specify name of the m3u file

## rate
Allows you to set a rating to a track, and album, or whatever.

Use:
rate <search-criteria> <number>
rate --current <number>  //rates the currently playing file

## config
Opens up the config file in your default text editor.

Stuff you can configure:
Rating scale: 0 is unrated, 1 is lowest, and you can pick the highest value.
Library path: The path to the folder that contains all your music.
Log files: GOODLOG and BADLOG for normal stuff and errors.


*Something I want to do: is to pipe the results of a search into another command.*

## synonym
Allows you to add a synonym to a term. Like:
synonym <old term> <new term>

So that any searches that match the <new term> will also link to the original and vice versa.
Allows synonyms for tags, like:
synonym arrangecover remix

--remove: delete the relationship

## subtag
Allows you to attach a tag as a subtag of another. So if you say:

subtag electro glitch-hop

then glitch-hop is now under electro and searches for #electro will also show results with the #glitch-hop tag.

--remove: delete the relationship

## autotag

Lets you automatically tag some tracks based on their metadata. Also add some rules to specify what to name a tag.

Use:
autotag <search-criteria> [rules]

## similar
Finds songs similar to a specific song.

This needs some ML stuff. Do it later.

## update

To help deal with changes to the actual files in your database (like if you delete them, move them or change metadata.)

-f="file_with_the_updated_details"

## favorites

Ontag will save your most used commands into a file so that you can hit them again without typing so much.
Or you can manually save them. Especially the really long and complicated ones.

On its own, it displays all your saved favorite commands.
Then you can execute them with something like:
ontag favorites 1
ontag favorites 5

Stuff like that. Shorten to 'fav'?

# Some notes over here

So I've used TinyDB for the database system in here.
I've used stat instead of lstat so that we can have links to file act the same as the files themselves.

## Stuff I want to be able to do in here

- Play songs from within the application
- Create playlists -- both permanent and temporary
- Rate songs
  - While they're playing -- maybe keep a variable called 'now-playing' that can be updated easily?
- Track play count and last-played

- Run some ML algorithms on this and see what pops out
