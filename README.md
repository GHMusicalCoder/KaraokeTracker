# KaraokeTracker
Process and Track my Karaoke collection

## Project Plan
* Project created in Linux (for linux)
1. Go thru excess folder, and undo all zip files, and record in temp db the file name and locations
2. Go thru the start folder and unzip all files
 Confirm all files are in cdg/mp3 format (ie 2 files with same name)
 All zip files should be deleted (unzipped and then removed)
3. Rename files to a standard format (artist name [no comma] - song title (ft artist)
 no comma means that you have The Beatles and Billy Joel - not Joel, Billy
 pulling the song names will be somewhat tricky as they can be in a few different formats
  there will have to be some processes in place for approving said entries
   part of approval can be to verify artist name in db
4. If artist/song title valid (ie not in DB) then store in db and proceed to step 6
5. If artist/song title exist - then delete  (this should only be because of a mis-named original item)
6. Delete all the same artist/song title combos from excess
7. Zip up new files into correct zip files and move them into appropriate folder structure
 Want to limit it so that there is not more than 50 artist to any given folder so when the system sees that **M** folder has 50 artists, it will split **M** into 2 folders with roughly 25 artists in each folder (based on current names)

## Considerations
Start with a master list of songs and artists from the excess files - instead of searching every file every time - I can look through this list and speed up as it has all the files. If I track the file name/location, then it would be easy to remove the duplicate files.
Try to do some type of misspell check - so if I come across a billy joel and billy jeol it would flag this.



