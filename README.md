# KaraokeTracker
Process and Track my Karaoke collection

# Project Plan

Read the Karaoke files from a start folder...

    Confirm all files are in cdg/mp3 format (so there should be 2 files)
        any zip files, should be unzipped to original files and then deleted
    Rename the files to a standard format
        NOTE this can probably require several possible options due to the possibility of being artist-title or title-artist, etc
        NOTE may require an approval stage (which can be augmented by an artist search in the DB to see if the artist already exists - thus allowing auto approval for the same artist)
    Store said file names and convention information into a DB (used for mapping purposes across multiple computers)
        NOTE that the DB will also be set up for the music system I want to design later, so keep in mind you will want a fully robust DB to handle this - not just for karaoke
        NOTE due to possible file naming conventions, currently named files may already exist so delete those from the start folder as well
    Go through excess files, and delete all files that match both artist and song

Some possible improvements -

    Start with a master list of songs and artists from the excess files - instead of searching every file every time - I can look through this list and speed up as it has all the files. If I track the file name/location, then it would be easy to remove the duplicate files.
    Try to do some type of misspell check - so if I come across a billy joel and billy jeol it would flag this.



