from db import db

class Media(db.Model):
    __tablename__ = 'medias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(250), nullable=False) 
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))

    artist = db.relationship("Artist", backref="media")
    
    def __init__(self, name = None, artist_id = None, media_dict = None):
        self.name = name
        self.artist_id = artist_id
        if media_dict:
            self.name = media_dict['trackName']
            self.artist_id = media_dict['artistId']

    def __repr__(self):
        return "{media_name} by {artist_name}".format(
            media_name = self.name, 
            artist_name = self.artist.name
        )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    main_genre = db.Column(db.String(250))


    def __init__(self, id = None, name = None, main_genre = None, artist_dict = None):
        self.id = id
        self.name = name
        self.main_genre = main_genre
        if artist_dict:
            self.id = artist_dict['results'][0]['artistId']
            self.name = artist_dict['results'][0]['artistName']
            self.main_genre = artist_dict['results'][0]['primaryGenreName']


    def __repr__(self):
        return "{artist} has {no} media(s):\n {detail}".format(
            artist = self.name,
            no = len(self.media), 
            detail = "\n".join([str(media) for media in self.media])
        ) 

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()