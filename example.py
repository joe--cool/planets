from planets import Planet, Tableau, Player, Coordinate, Planets

tableau = Tableau(Coordinate(900, 900))
players = [
    Player("Aaron"),
    Player("Peter"),
]

p = Planets(tableau, players, 10)

print("\nPlayer planets:")
for planet in p.player_planet_list:
    print(planet)

print("\nNon-player planets:")
for planet in p.planet_list:
    print(planet)

print("\nTest Subscriptions:")
for planet in p.get_all_planets():
    planet.subscribe(lambda x: print(f"{x} - {x.owner}"))

print("\nUpdate Onwership:")
p.planet_list[0].set_owner(players[1])
