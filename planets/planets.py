from dataclasses import dataclass
import random
from enum import Enum
from typing import Self, Optional


@dataclass
class Coordinate:
    """
    A class for keeping track of coordinates within the game.
    """

    x: int
    y: int


@dataclass
class Area:
    """
    A class for keeping track of an area within the game.
    """

    upper_left: Coordinate
    bottom_right: Coordinate


@dataclass
class Tableau(Area):
    """
    A class represeting the game board.  The upper left coordinate is always (0, 0).  When
    creating a new Tableau, only the bottom right coordinate needs to be specified.  This
    effectively sets the playing space.
    """

    def __init__(self: Self, bottom_right: Coordinate):
        # Fix the bottom left coordinate to (0, 0)
        upper_left = Coordinate(0, 0)
        super().__init__(upper_left, bottom_right)

    def get_size(self: Self) -> tuple[int, int]:
        """
        Returns a tuple of the size of the tableau.  Helpful for passing to
        pygame.display.set_mode().
        """
        return (self.bottom_right.x, self.bottom_right.y)


class PlanetSize(Enum):
    """
    An enum representing the size of a planet.
    """

    SMALL = 25
    MEDIUM = 50
    LARGE = 75


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
    home_player: Optional["Player"] = None,
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
                area.upper_left.x + min_distance, area.bottom_right.x - min_distance
            ),
            random.randint(
                area.upper_left.y + min_distance, area.bottom_right.y - min_distance
            ),
        )

        planet = Planet(coordinate, planet_size, home_player)

    return planet


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
    """
    A class representing a player in the game.
    """

    def __init__(self: Self, name: str):
        self.name = name

    def set_home_planet(self: Self, planet: "Planet"):
        self.home_planet = planet

    def __str__(self: Self):
        return f"Player(name={self.name})"


class Planet(object):
    """
    A class representing a planet in the game.
    """

    def __init__(
        self: Self,
        coordinate: Coordinate,
        planet_size: PlanetSize,
        home_player: Optional[Player] = None,
    ):
        if not isinstance(planet_size, PlanetSize):
            raise ValueError(
                "Invalid planet size. Must be a valid PlanetSize enum value."
            )

        self.coordinate = coordinate

        self.planet_size = planet_size
        self.home_player = home_player

        if home_player:
            self.owner = home_player
            home_player.set_home_planet(self)
        else:
            self.owner = None

    def set_owner(self: Self, player: Player) -> None:
        self.owner = player

    def __str__(self: Self):
        if self.home_player:
            return f"Planet(coordinate={self.coordinate}, planet_size={self.planet_size}, home_player={self.home_player.name}))"
        else:
            return (
                f"Planet(coordinate={self.coordinate}, planet_size={self.planet_size}))"
            )


class Planets(object):
    """
    A class for creating and keeping track of all the planets in the game.  This is intended to be
    the core state machine for the game.
    """

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

        # Create home planets for each player
        for player in self.players:
            player_planet = self.create_planet(
                planet_size=PlanetSize.MEDIUM, home_player=player
            )
            self.player_planet_list.append(player_planet)

        # Create the rest of the planets
        for i in range(number_of_planets):
            self.planet_list.append(self.create_planet())

    def get_all_planets(self: Self) -> list[Planet]:
        return self.player_planet_list + self.planet_list

    def create_planet(
        self: Self,
        planet_size: PlanetSize | list[PlanetSize] = list(PlanetSize),
        home_player: Optional[Player] = None,
    ) -> None:
        return create_random_planet(
            self.tableau,
            min_distance=self.min_distance,
            planet_size=planet_size,
            collision_list=self.get_all_planets(),
            home_player=home_player,
        )


if __name__ == "__main__":
    tableau = Tableau(Coordinate(150, 150))
    players = [
        Player("Aaron"),
        Player("Peter"),
    ]

    p = Planets(tableau, players, 10)

    print("Player planets:")
    for planet in p.player_planet_list:
        print(planet)

    print("Non-player planets:")
    for planet in p.planet_list:
        print(planet)

    print("Player 1's planet:")
    print(players[0].home_planet)
