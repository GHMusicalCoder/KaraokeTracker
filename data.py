import sqlite3
import sys
from contextlib import contextmanager


def db_first_launch(DB):
    try:
        conn = sqlite3.connect(DB)
    except:
        sys.exit('Error Code DB-X for ' + DB)


@contextmanager
def access_db(DB):
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        yield cursor
    finally:
        conn.commit()
        conn.close()


def make_tables(DB):
    with access_db(DB) as cursor:
        # Turn On Foreign Keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        # Artist table - ID and Artist Name (maybe additional items later)
        cursor.execute("CREATE TABLE if not exists Artists (ArtistID INTEGER PRIMARY KEY, Artist TEXT);")
        # Temp Artist table - this may or may not be used - depending on how I work this program
        cursor.execute("CREATE TABLE if not exists TempArtists (TempID INTEGER, Name TEXT);")
        # Artist Link - this is for bad spellings of name (Bily Jeol vs Billy Joel) - to automate repair for songs
        cursor.execute(
            """CREATE TABLE if not exists ArtistLink 
                (LinkID INTEGER PRIMARY KEY, Link TEXT, ArtistID INTEGER, 
                FOREIGN KEY(ArtistID) REFERENCES Artists(ArtistID));""")
        # Song Table - ID, Name, PrimaryArtist (link to Artist), IsMusic (for later linking to DJ MP3s)
        # -- IsKaraoke (to separate Karaoke vs DJ MP3)
        cursor.execute(
            """CREATE TABLE if not exists Song 
                (SongID INTEGER PRIMARY KEY, Song TEXT, PrimaryArtist INTEGER,
                IsMusic INTEGER, IsKaraoke INTEGER, FOREIGN KEY(PrimaryArtist) REFERENCES Artists(ArtistID));""")
        # SongFeaturing - Links Songs with Featuring Artists (ie Love the Way You Lie - Eminem w/ Rhianna)
        cursor.execute(
            """CREATE TABLE if not exists SongFeaturing 
                (SongID INTEGER, ArtistID INTEGER, PRIMARY KEY (SongID, ArtistID),
                FOREIGN KEY(ArtistID) REFERENCES Artists(ArtistID),
                FOREIGN KEY(SongID) REFERENCES Song(SongID));""")
        # KaraokeVendors - Main Karaoke Track Vendors and their Primary Abbreviation for TrackLinks
        cursor.execute(
            """CREATE TABLE if not exists KaraokeVendors 
                (VendorID INTEGER PRIMARY KEY, Vendor TEXT, PrimaryAbbreviation TEXT);""")
        # KaraokeAbbreviations - Additional Abbreviations (Like SunFly has SF and SFGG or SFKK)
        cursor.execute(
            """CREATE TABLE if not exists VendorAbbreviations 
                (VendorID INTEGER, Abbreviation TEXT UNIQUE,
                FOREIGN KEY(VendorID) REFERENCES KaraokeVendors(VendorID));""")
        # KaraokeDisks - The individual Vendor Discs
        cursor.execute(
            """CREATE TABLE if not exists KaraokeDisks 
                (DiscID INTEGER PRIMARY KEY, VendorID INTEGER, Disc TEXT,
                FOREIGN KEY(VendorID) REFERENCES KaraokeVendors(VendorID));""")
        # KaraokeTracks - The individual Tracks - links Song to Karaoke Disc
        cursor.execute(
            """CREATE TABLE if not exists KaraokeTracks
                (TrackID INTEGER PRIMARY KEY, SongID INTEGER, DiscID INTEGER, TrackNo INTEGER, HasVocal INTEGER,
                FOREIGN KEY(SongID) REFERENCES Song(SongID), FOREIGN KEY(DiscID) REFERENCES KaraokeDiscs(DiscID));""")
        # At this point - we can only add NEW Tables above - (as we have added data) - changes to existing tables
        # require us to use ALTER TABLE

    print("DB Tables have been created/verified.")


def has_artist(DB, artist):
    with access_db(DB) as c:
        c.execute("SELECT * FROM Artist WHERE Artists = {0}".format(artist))
        artist_exists = c.fetchone()
        return artist_exists
