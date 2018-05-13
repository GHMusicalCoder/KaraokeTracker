import sqlite3
import sys
from contextlib import contextmanager


class TrackingDB(object):
    """
    This class should handle ALL access to the database.
    """

    def __init__(self, db_file, first_run=False):
        """
        Initialize the connection to our database
        If first run is true, we'll build the DB and create the initial table, otherwise
        we'll read the value of version to set the db version and then run the db update function
        :param db_file: this is the name/location of the database file
        :param first_run: a boolean that tells us if we need to create the db first
        """
        self.database = db_file
        self.db_version = 0
        self.db_valid = True
        if first_run:
            # the database doesn't exist - so we will initiate the file and add the kt_main table
            print("*" * 60)
            print("Initializing the database file")
            print()
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")
                cursor.execute("CREATE TABLE if not exists kt_main (version INTEGER);")
                cursor.execute("INSERT INTO kt_main (version) VALUES (0);")
                conn.commit()
                conn.close()
            except Exception as e:
                self.db_valid = False
        else:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT version FROM kt_main;")
            value = cursor.fetchall()
            self.db_version = value[0][0]
            conn.close()

        self.db_valid = self.db_update_all()

    def db_update_all(self):
        """
        processes through various updates
        :: idea here is that version starts at 0 on database creation, and we'll do a check to see if version is
        :: less than 1, and run the table creations and then update version to 1
        :: THEN, on the next update, we'll check if version is below 2, and then run that update (so that this will
        :: run on every class instantiation, but will only update the tables if the version dictates an update
        :: ALL THAT NEEDS TO BE MODIFIED IS THE FINAL ENTRY TO UPDATE THE VERSION (and then insert the new version
        :: before it)
        :return: True if no issues, otherwise false
        """

        if self.db_version > 1:
            # run DB update 1
            if not self.db_update_one():
                return False

        if self.db_version == 1:
            return True

    def db_update_one(self):
        """
        first database update
        :return: True if no problem with update - otherwise returns false
        """
        return True

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
