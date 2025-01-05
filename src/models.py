from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = "People"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
    img = db.Column(db.String(250), unique=False, nullable=True)
    skills = db.Column(db.String(100), unique=False, nullable=True)
    color_eyes = db.Column(db.String(10), unique=False, nullable=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
class FavoritePeople(db.Model):
    __tablename__ = "Fav_People"

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('User.id'))
    id_people = db.Column(db.Integer, db.ForeignKey('People.id'))

    people = db.relationship("People", backref="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "people": self.people.serialize() if self.people else None
        }
    
class Planet(db.Model):
    __tablename__ = "Planet"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
    img = db.Column(db.String(250), unique=False, nullable=True)
    climate = db.Column(db.String(50), unique=False, nullable=True)
    population = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
class FavoritePlanet(db.Model):
    __tablename__ = "Fav_Planet"

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('User.id'))
    id_planet = db.Column(db.Integer, db.ForeignKey('Planet.id'))

    planet = db.relationship("Planet", backref="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "planet": self.planet.serialize() if self.planet else None
        }