"""
This is the sqlite database class that handles the database access for the Karaoke Tracker
written by MusicalCoder
written on 2018-05-13 (@Pycon)
"""
import sqlite3
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
        self.database = str(db_file)
        self.db_version = 0
        self.db_valid = True
        if first_run:
            # the database doesn't exist - so we will initiate the file and add the kt_main table
            self.print_class_message(f"Initializing the database file {self.database}")
            try:
                conn = sqlite3.connect(self.database)
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")
                cursor.execute("CREATE TABLE if not exists main (version INTEGER);")
                cursor.execute("INSERT INTO main (version) VALUES (0);")
                conn.commit()
                conn.close()
            except Exception as e:
                self.db_valid = False
                self.print_class_message(f"Error initializing database: {e}")
        else:
            self.print_class_message("Checking for database updates...")
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute("SELECT version FROM main;")
            value = cursor.fetchall()
            self.db_version = value[0][0]
            conn.close()

        self.db_valid = self.db_update_all()

    def print_class_message(self, message, close=True, open=True):
        if open:
            print("*" * 80)
        print(message)
        if close:
            print()

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

        if self.db_version < 1:
            # run DB update 1
            if not self.db_update_one():
                return False

        # add new update if here - if self.db_version < 2:
        if self.db_version == 1:    # change this to the new update # when making a new update
            return True

    def db_update_one(self):
        """
        first database update - creating the following tables:
        * Artists - the table of artists
        * ArtistAlias - the table of misspelled artists and the associated artist
        * Song - the table of songs
        * SongFeat - additional artists associated with song (Uptown Funk - Mark Ronson ft Bruno Mars)
        * KaraokeVendors - table of karaoke vendors with primary disc abbreviation
        * KaraokeAbbreviations - table of karaoke vendor disc abbreviations
        :return: True if no problem with update - otherwise returns false
        """
        try:
            self.print_class_message("Applying Database Update #1...", close=False)
            with self.access_db() as c:
                print("   Creating Artist Table...")
                c.execute("CREATE TABLE if not exists Artists (ArtistID INTEGER PRIMARY KEY, Artist TEXT);")
                print("   Creating Index for Artist Table")
                c.execute("CREATE INDEX if not exists IX_Artists_Artist ON Artists (Artist);")
                print("   Creating Artist Alias table...")
                c.execute("CREATE TABLE if not exists ArtistAlias "
                          "(ArtistAliasID INTEGER PRIMARY KEY, ArtistAlias TEXT, ArtistID INTEGER,"
                          "FOREIGN KEY(ArtistID) REFERENCES Artists(ArtistID));")
                print("   Creating Index for Artist Alias Table")
                c.execute("CREATE INDEX if not exists IX_ArtistAlias_ArtistAlias ON ArtistAlias (ArtistAlias);")
                print("    Creating Song table...")
                c.execute("CREATE TABLE if not exists Song "
                          "(SongID INTEGER PRIMARY KEY, Song TEXT, PrimaryArtist INTEGER,"
                          "IsMusic INTEGER, IsKaraoke INTEGER,"
                          "FOREIGN KEY(PrimaryArtist) REFERENCES Artists(ArtistID));")
                print("   Creating Index for Songs Table")
                c.execute("CREATE INDEX if not exists IX_Song_Song ON Song (Song);")
                print("    Creating Song Featuring table...")
                c.execute("CREATE TABLE if not exists SongFeaturing"
                          "(SongID INTEGER, ArtistID INTEGER, PRIMARY KEY (SongID, ArtistID),"
                          "FOREIGN KEY(ArtistID) REFERENCES Artists(ArtistID),"
                          "FOREIGN KEY(SongID) REFERENCES Song(SongID));")
                print("    Creating Karaoke Vendors table...")
                c.execute("CREATE TABLE if not exists KaraokeVendors"
                          "(VendorID INTEGER PRIMARY KEY, Vendor TEXT);")
                print("   Creating Index for KaraokeVendors Table")
                c.execute("CREATE INDEX if not exists IX_KaraokeVendors_Vendor ON KaraokeVendors (Vendor);")
                print("    Creating Karaoke Abbreviations table...")
                c.execute("CREATE TABLE if not exists VendorAbbreviations"
                          "(VendorID INTEGER, Abbreviation TEXT UNIQUE, IsPrimaryAbbreviation INTEGER,"
                          "FOREIGN KEY(VendorID) REFERENCES KaraokeVendors(VendorID));")
                print("   Creating Index for VendorAbbreviations Table")
                c.execute("CREATE INDEX if not exists IX_VendorAbbreviations_Abbreviation"
                          "ON VendorAbbreviations (Abbreviation);")
                print("    Creating Song Alias table...")
                c.execute("CREATE TABLE if not exists SongAlias"
                          "(SongAliasID INTEGER PRIMARY KEY, SongID INTEGER, SongAlias TEXT,"
                          "FOREIGH KEY(SongID) REFERENCES Song(SongID));")
                print("   Creating ICREATEndex for SongAlias Table")
                c.execute("CREATE INDEX if not exists IX_SongAlias_SongAlias ON SongAlias (SongAlias);")
                print("    Creating Karaoke Disc table...")
                c.execute("CREATE TABLE if not exists KaraokeDiscs"
                          "(DiscID INTEGER PRIMARY KEY, VendorID INTEGER, Disc TEXT,"
                          "FOREIGN KEY(VendorID) REFERENCES KaraokeVendors(VendorID));")
                print("    Creating Karaoke Track table...")
                c.execute("CREATE TABLE if not exists KaraokeTracks"
                          "(TrackID INTEGER PRIMARY KEY, SongID INTEGER, DiscID INTEGER,"
                          "TrackNo INTEGER, HasVocal INTEGER, FOREIGN KEY(SongID) REFERENCES Song(SongID),"
                          "FOREIGN KEY(DiscID) REFERENCES KaraokeDiscs(DiscID));")
                c.execute("UPDATE kt_main SET version = 1;")
                self.print_class_message("All #1 updates have been applied successfully", open=False)
            return True
        except Exception as e:
            self.print_class_message(f"Problem encountered {e}")
            return False

    def get_artist(self, name):
        """
        first look through artist table for the artist name, then check the artist alias table
        :param name: name of the artist we are looking for
        :return: either artist id or 0 if not found
        """
        with self.access_db() as sql:
            sql.execute("select ArtistID from Artists where Artist = '{0}'".format(name))
            data = sql.fetchone()
            if data:
                # data should be a tuple with (id, blank)
                return data[0]
            else:
                # now we test alias table
                sql.execute("select ArtistID from ArtistAlias where ArtistAlias = '{0}'".format(name))
                data = sql.fetchone()
                if data:
                    return data[0]

        return 0

    @contextmanager
    def access_db(self):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            yield cursor
        finally:
            conn.commit()
            conn.close()
