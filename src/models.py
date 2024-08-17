from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    favoritos = db.relationship('Favorite', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_creacion": self.fecha_creacion
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    clima = db.Column(db.String(100))
    terreno = db.Column(db.String(100))
    poblacion = db.Column(db.Integer)
    diametro = db.Column(db.Integer)
    periodo_orbital = db.Column(db.Integer)
    periodo_rotacion = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion,
            "diametro": self.diametro,
            "periodo_orbital": self.periodo_orbital,
            "periodo_rotacion": self.periodo_rotacion
        }

    favoritos = db.relationship('Favorite', backref='planet', lazy=True)

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    altura = db.Column(db.Integer)
    peso = db.Column(db.Integer)
    genero = db.Column(db.String(20))
    especie = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "peso": self.peso,
            "genero": self.genero,
            "especie": self.especie
        }

    favoritos = db.relationship('Favorite', backref='character', lazy=True)

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }
