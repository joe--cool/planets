from dataclasses import dataclass
import random
from enum import Enum, auto
from typing import Self


@dataclass
class Coordinate:
    x: int
    y: int


@dataclass
class Area:
    bottom_left: Coordinate
    upper_right: Coordinate


@dataclass
class Tableau(Area):
    def __init__(self: Self, upper_right: Coordinate):
        # Fix the bottom left coordinate to (0, 0)
        bottom_left = Coordinate(0, 0)
        super().__init__(bottom_left, upper_right)


class PlanetSize(Enum):
    SMALL = 5
    MEDIUM = 10
    LARGE = 15


def check_planet_size(planet_size: PlanetSize | list[PlanetSize]):
    if isinstance(planet_size, list) and not all(
        isinstance(p, PlanetSize) for p in planet_size
    ):
        raise ValueError(
            "Invalid planet size. If using a list for planet_size all values must a PlanetSize enum."
        )

    if not (isinstance(planet_size, list)) and not isinstance(planet_size, PlanetSize):
        raise ValueError("Invalid planet size. Must be a valid PlanetSize enum value.")


def create_random_planet(
    area: Area,
    min_distance: int,
    planet_size: PlanetSize | list[PlanetSize] = list(PlanetSize),
    collision_list: list["Planet"] = [],
):
    """
    Create random planet within the given area.
    """
    check_planet_size(planet_size)

    planet = None

    if isinstance(planet_size, list):
        planet_size = random.choice(planet_size)

    while planet is None or check_for_colision(planet, collision_list, min_distance):
        # Create a planet with random coordinates
        coordinate = Coordinate(
            random.randint(
                area.bottom_left.x + planet_size.value,
                area.upper_right.x - planet_size.value,
            ),
            random.randint(
                area.bottom_left.y + planet_size.value,
                area.upper_right.y - planet_size.value,
            ),
        )

        planet = Planet(coordinate, planet_size)

    return Planet(coordinate, planet_size)


def check_for_colision(
    planet: "Planet", collision_list: list["Planet"], min_distance: int
):
    """
    Check if the planet collides with any other planet in the list.
    """

    for other_planet in collision_list:
        if (planet.coordinate.x - other_planet.coordinate.x) ** 2 + (
            planet.coordinate.y - other_planet.coordinate.y
        ) ** 2 < min_distance**2:
            return True

    return False


class Player(object):
    def __init__(self: Self, name: str):
        self.name = name

    def set_home_planet(self: Self, planet: "Planet"):
        self.home_planet = planet


class Planet(object):
    def __init__(self: Self, coordinate: Coordinate, planet_size: PlanetSize):
        if not (isinstance(planet_size, list)) and not isinstance(
            planet_size, PlanetSize
        ):
            raise ValueError(
                "Invalid planet size. Must be a valid PlanetSize enum value."
            )

        self.coordinate = coordinate
        self.planet_size = planet_size
        self.owner = None

    def set_owner(self: Self, player: Player):
        self.owner = player

    def __str__(self: Self):
        return f"Planet(coordinate={self.coordinate}, planet_size={self.planet_size}))"


class Planets(object):
    def __init__(
        self: Self,
        tableau: Tableau,
        players: list[Player],
        number_of_planets: int = 10,
        min_distance: int = 10,
    ):
        self.tableau = tableau
        self.players = players
        self.min_distance = min_distance
        self.player_planet_list = []
        self.planet_list = []

        random.shuffle(self.players)

        for player in self.players:
            player_planet = self.create_planet()
            player.set_home_planet(player_planet)
            player_planet.set_owner(player)
            self.player_planet_list.append(player_planet)

        for i in range(number_of_planets):
            self.planet_list.append(self.create_planet())

    def get_all_planets(self: Self):
        return self.player_planet_list + self.planet_list

    def create_planet(
        self: Self, planet_size: PlanetSize | list[PlanetSize] = list(PlanetSize)
    ):
        return create_random_planet(
            self.tableau,
            min_distance=self.min_distance,
            planet_size=planet_size,
            collision_list=self.get_all_planets(),
        )


if __name__ == "__main__":
    tableau = Tableau(Coordinate(150, 150))
    players = [
        Player("Aaron"),
        Player("Peter"),
    ]

    p = Planets(tableau, players, 10)
