from planets import Planet, Tableau, Player, Coordinate, Planets

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
