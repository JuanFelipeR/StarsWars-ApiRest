from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Modelo de Usuario
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    favorites_characters = relationship("FavoriteCharacter", backref="user")
    favorites_planets = relationship("FavoritePlanet", backref="user")
    favorites_vehicles = relationship("FavoriteVehicle", backref="user")

    def serialize(self):
        return {

            "id":self.id,
            "username":self.username,
            "email":self.email,
            "favorites_characters": [fc.character.serialize() for fc in self.favorites_characters],
            "favorites_planets": [fp.planet.serialize() for fp in self.favorites_planets],
            "favorites_vehicles": [fv.vehicle.serialize() for fv in self.favorites_vehicles],
        }

# Modelo de Personaje
class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    birth_year: Mapped[str] = mapped_column(String(20))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)

    planet = relationship("Planet", backref="residents")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "planet_id": self.planet_id
            # "vehicles": [vehicle.serialize() for vehicle in self.vehicles] si quiero incluir los vehiculos de cada piloto cuando character_id y vehicle_id coincidan
        }

# Modelo de Planeta
class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    population: Mapped[int] = mapped_column(nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
        }
# Modelo de Vehículo
class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50))
    passengers: Mapped[int] = mapped_column(nullable=True)
    pilot_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)

    pilot = relationship("Character", backref="vehicles") #relacion inversa: mirar character.serialize()

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "model":self.model,
            "passengers":self.passengers,
            "pilot_id":self.pilot_id
        }

# Modelo de Favoritos (uno para cada tipo, para simplificar)
class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)

    character = relationship("Character")

class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    planet = relationship("Planet")

class FavoriteVehicle(db.Model):
    __tablename__ = "favorite_vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=False)

    vehicle = relationship("Vehicle")