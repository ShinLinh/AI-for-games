from random import choice

class TacticalAI(object):

    def update(self, gameinfo):
        if gameinfo.my_fleets:
            return
        else:
            if gameinfo.my_planets and gameinfo.not_my_planets:
                src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)
        
                weakest_planet = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)
                closest_planet = list(gameinfo.not_my_planets.values())[0]
                for planet in gameinfo.not_my_planets.values():
                    if planet != closest_planet:
                        if planet.distance_to(src) < closest_planet.distance_to(src):
                            closest_planet = planet

                most_productive_planet = max(gameinfo.not_my_planets.values(), key=lambda p: p.growth_rate)
        
                potential_targets = []

                potential_targets.append(weakest_planet)
                potential_targets.append(closest_planet)
                potential_targets.append(most_productive_planet)

                dest = choice(potential_targets)

                gameinfo.planet_order(src, dest, src.num_ships)
                gameinfo.log("I'll send %d ships from planet %s to planet %s" % (src.num_ships, src, dest))