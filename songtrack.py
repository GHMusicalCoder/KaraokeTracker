"""
This is the song track class - will handle all aspects of a song track
written by MusicalCoder
written on 2018-05-13 (@ Pycon)
"""


class SongTrack(object):
    def __init__(self):
        self.artistid = 0
        self.songid = 0
        self.artist = ''
        self.song = ''
        self.abbr = ''
        self.disc = ''
        self.track = ''
        self.artist_alias = ''
        self.song_alias = ''
