
class AggressiveAI(object):
    """AI that actively tries to beat the enemy"""
    
    def update(self, gameinfo):
        if gameinfo.my_fleets:
            return
        else:
            if gameinfo.my_planets and gameinfo.not_my_planets:
                # Copy the list of uncontrolled planets into a temporary list
                targets = list(gameinfo.not_my_planets.values())
                max_targets = []
                min_targets = []
                max_product_targets = []
                # Get the controlled planet with the highest number of ships as source
                src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)
                
                # Get a list of 2 planets with the highest number of ships while there are still available planets to target
                while len(max_targets) < 2 and len(targets) > 0:
                    max_target = max(targets, key=lambda p: p.num_ships)  
                    targets.remove(max_target) 

                    max_target_ships = max_target.num_ships + src.distance_to(max_target) * max_target.growth_rate
                    # Choose only planets that can be taken immediately
                    while max_target_ships > src.num_ships* 0.75 and len(targets) > 0:
                        max_target = max(targets, key=lambda p: p.num_ships)
                        max_target_ships = max_target.num_ships + src.distance_to(max_target) * max_target.growth_rate 
                        targets.remove(max_target)
                    max_targets.append(max_target)
                
                # Reset the list of targets
                targets = list(gameinfo.not_my_planets.values())
                    
                # Get a list of 2 planets with the highest production speed while there are still available planets to target
                while len(max_targets) < 2 and len(targets) > 0:
                    max_target = max(targets, key=lambda p: p.growth_rate)  
                    targets.remove(max_target) 
                    max_target_ships = max_target.num_ships + src.distance_to(max_target) * max_target.growth_rate
                    # Choose only planets that can be taken immediately
                    while max_target_ships > src.num_ships* 0.75 and len(targets) > 0:
                        max_target = max(targets, key=lambda p: p.growth_rate)
                        max_target_ships = max_target.num_ships + src.distance_to(max_target) * max_target.growth_rate 
                        targets.remove(max_target)
                    max_product_targets.append(max_target)

                # Reset the list of targets
                targets = list(gameinfo.not_my_planets.values())

                # Get a list of 2 planets with the lowest number of ships while there are still available planets to target
                while len(min_targets) < 2 and len(targets) > 0:
                    min_target = min(targets, key=lambda p: p.num_ships)  
                    targets.remove(min_target)
                    min_target_ships = min_target.num_ships + src.distance_to(min_target) * min_target.growth_rate
                    while min_target_ships > src.num_ships* 0.75 and len(targets) > 0:
                       min_target = max(targets, key=lambda p: p.num_ships) 
                       min_target_ships = min_target.num_ships + src.distance_to(min_target) * min_target.growth_rate
                       targets.remove(min_target)
                    min_targets.append(min_target)
                
                # Check if there are available targets in the min/max lists
                if len(min_targets) == len(max_targets) == 0:
                    # Target the planet with the lowest number of ships
                    dest = min(targets, key=lambda p: p.num_ships)
                else:
                    # Target the planet within the min/max list that is the closest to the source planet
                    choices = {}
                
                    for target in max_targets:
                        choices.update({target:src.distance_to(target)})
                    for target in min_targets:
                        choices.update({target:src.distance_to(target)})
                    for target in max_product_targets:
                        choices.update({target:src.distance_to(target)})            
                    dest =  min(choices, key=lambda k: choices[k])

                # launch new fleet if there are enough ships
                if src.num_ships > 10:
                    gameinfo.planet_order(src, dest, int(src.num_ships * 0.75) )     

