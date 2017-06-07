'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY, COLOR_NAMES
from math import sin, cos, radians
from random import random, randrange, choice, uniform
from path import Path
from projectile import Projectile, PROJECTILE_TYPES, WEAPON_MAX_ROUNDS
from copy import copy
AGENT_MODES = [
    'patrol',
    'wander',
    'engage'
]

AGENT_ENGAGE_SUBMODE = [
    'reload',
    'fire'
]

AGENT_PATROL_SUBMODE = [
    'move',
    'observe'
]

WEAPON_FIRING_SPEED = {
        'rifle' : 0.7,
        'rocket' : 4.0,
        'handgun' : 0.3,
        'hand_grenade' : 3.0
}

WEAPON_RELOAD_SPEED = {
        'rifle' : 2.5,
        'rocket' : 4.0,
        'handgun' : 2.0,
        'hand_grenade' : 3.0    
}

class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.7,
        ### ADD 'normal' and 'fast' speeds here
        'normal': 1.0,
        'fast': 1.5,
    }
    
    

    def __init__(self, world=None, scale=20.0, mass=1.0, mode='seek'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        self.sub_mode = 'fire'
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D() # current steering force
        self.acceleration = Vector2D()  # current acceleration
        self.mass = mass
        # limits?
        # self.max_speed = 500.0
        # data for drawing this agent
        self.color = choice(list(COLOR_NAMES.keys())) 
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        self.path = Path(0, 0, 0, 0, 0, True)
        self.path.add_way_pt(Vector2D(100.0, 100.0))
        self.path.add_way_pt(Vector2D(400.0, 100.0))
        self.path.add_way_pt(Vector2D(400.0, 400.0))  
        self.path.add_way_pt(Vector2D(100.0, 400.0))

        self.waypoint_threshold = 5.0
        self.wander_dist = 500.0
        self.wander_radius = 50.0
        # New wander info
        self.wander_target = Vector2D(1,0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale
        
        # Force and speed limiting
        self.max_speed = 10.0 *scale
        self.max_force = 500.0

        self.show_info = False
        
        #self.current_target = None

        # minimum distance from enemies
        self.safe_radius = 70.0
        self.bounding_radius = 50.0
        self.tagged = False

        # Whether the agent is a target or not. This changes how it is rendered
        self.is_a_target = False
        # The radius of the agent if it is a target
        self.target_radius = 20.0
        # Maximum movement speed when in patrol mode to simulate resting
        self.rest_speed = 100.0
        # Current weapon type, determines the aim algorithm and the projectile fired
        self.gun_type = 'rifle'
        
        # The timer for weapon's cooldown for each shot
        self.firing_timer = 0.0
        # The timer for reloading to simulate the time needed to reload a weapon
        self.reload_timer = copy(WEAPON_RELOAD_SPEED[self.gun_type])
        # The timer for how long the hunter stays at a patrol waypoint to simulate "checking the position"
        self.patrol_timer = 2.0
        # The agent's hitpoint.
        self.HP = 10
        
        # The agent's inventory,indicating the ammo it has for each weapon
        self.weapon_ammunition_inventory = {
            'rifle' : 8,
            'rocket' : 1,
            'handgun' : 12,
            'hand_grenade' : 1
        }

    def calculate(self, delta):
        # reset the steering force
        mode = self.mode
        if mode == 'patrol':
            force = self.follow_path()
        elif mode == 'wander':
            if self.is_a_target:
                force = self.seek(self.world.hunter.pos)
            else:
                force = self.wander(delta)
        elif mode == 'engage':
            force = self.wander(delta)* 300 + self.separate_from_other() * 300
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        if self.is_a_target == False:
            self.tag_close_enemies(self.safe_radius)
            
            # Switch between modes depending on the availability of target bots/enemies in the world
            if len(self.world.target_bots) > 0:
                self.mode = 'engage'
            else:
                self.mode = 'patrol'
            
            if self.mode == 'engage':
                ammo = copy(self.weapon_ammunition_inventory[self.gun_type])
                # The agent cannot fire when in the middle of reloading (reload timer not at max), or has no ammo
                if ammo > 0 and self.reload_timer == WEAPON_RELOAD_SPEED[self.gun_type]:
                    self.sub_mode = 'fire'
                else:
                    self.sub_mode = 'reload'

            if self.sub_mode == 'fire' and self.mode == 'engage': 
                # The agent cannot shoot while the weapon is still on cooldown
                if self.firing_timer > 0.0:
                    self.firing_timer -= delta
                else:
                    self.shoot()
            # Reload when in the reload submode of the engage mode, or in patrol mode
            if self.sub_mode == 'reload' or self.mode == 'patrol':
                self.reload(delta)
        
        force = self.calculate(delta)
        force.truncate(self.max_force)
        self.acceleration = force/self.mass        
        # new velocity
        self.vel += self.acceleration * delta
        # check for limits of new velocity
        if self.is_a_target == False: 
            if self.mode == 'patrol':
                # If in 'move' submode, the agent moves a slower speed
                if self.sub_mode == 'move':
                    self.vel.truncate(self.rest_speed)
                else:
                    # During 'observe' submode, the agent stays at the waypoint for 2 seconds, then switch back to 'move mode'
                    if self.patrol_timer < 0:
                        self.sub_mode = 'move'
                        self.patrol_timer = 2.0
                    self.patrol_timer -= delta
            else:
                self.vel.truncate(self.max_speed)
        else:
            self.vel.truncate(self.max_speed)
        # update position except during the observe submode       
        if self.sub_mode != 'observe':
            self.pos += self.vel * delta
            # update heading is non-zero velocity (moving)
            if self.vel.length_sq() > 0.00000001:
                self.heading = self.vel.get_normalised()
                self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        egi.set_pen_color(name=self.color)
        if self.is_a_target != True:
            pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
            # draw it!
            egi.closed_shape(pts) 
        else:
            egi.circle(self.pos, self.target_radius)

        if self.mode == 'patrol':
            self.path.render()
        if self.show_info:
            s = 0.5
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            egi.white_pen()
            egi.line_with_arrow(self.pos + self.vel * s, self.pos + (self.force + self.vel) * s, 5)

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
## add panic distance (second)
        panic_distance = 130.0
## add flee calculations (first)
        desired_velocity = self.vel
        if self.pos.distance(hunter_pos) < panic_distance:
            desired_velocity = ((hunter_pos - self.pos).normalise() * self.max_speed).get_reverse()
        return (desired_velocity - self.vel)


    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''
## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
        return Vector2D()

    def randomise_path(self):
        cx = self.world.cx  
        cy = self.world.cy
        margin = min(cx, cy) * (1/6)
        self.path.create_random_path(2, 0, 0, cx, cy)

    def follow_path(self):
        path = self.path
        if path.looped is False:
            if path.is_finished():
                return self.arrive(path.current_pt(), 'normal')
            else:
                if self.pos.distance(path.current_pt()) < self.waypoint_threshold:
                    path.inc_current_pt()
                return self.seek(path.current_pt())
        else:
            if self.pos.distance(path.current_pt()) < self.waypoint_threshold:
                path.inc_current_pt()
            return self.arrive(path.current_pt(), 'normal')
                
    def shoot(self):
        if len(self.world.target_bots) > 0 and self.firing_timer <= 0 and self.weapon_ammunition_inventory[self.gun_type] > 0:
            target = self.world.target_bots[0]
            for agent in self.world.target_bots:
                if (self.pos - agent.pos).length() < (self.pos - target.pos).length():
                    target = agent

            hit = False
            out_of_bound = False
            delta = 0.0
            projected_bullet = None
            while hit == False and out_of_bound == False:
                #iterate every millisecond
                delta += 0.001
                # Get the projected position of the target after delta seconds
                projected_target_position = target.pos + target.vel*delta + (target.acceleration/2)*delta*delta
                # Get an unit vector from self.pos to projected position to shoot
                vector_to_target = (projected_target_position - self.pos).normalise()
                # Create a projected bullet
                projected_bullet = Projectile(self.world, self.gun_type, self.pos.copy(),vector_to_target)
                # Update the position of the bullet after delta seconds
                projected_bullet.update(delta)
                #Check whether the bullet hits or not
                if (projected_bullet.pos - projected_target_position).length() < 25.0:
                    hit = True
                # Check whether the bullet goes out of bound after delta seconds
                out_of_bound = self.world.out_of_bound(projected_bullet.pos)

            if hit == True:
                bullet = Projectile(self.world,self.gun_type,self.pos.copy(), projected_bullet.aim)
                self.world.projectiles.append(bullet)
                # Actually shoot the projectile
                bullet.fire()
                self.weapon_ammunition_inventory[self.gun_type] -= 1
                self.firing_timer = copy(WEAPON_FIRING_SPEED[self.gun_type])
                

    def wander(self, delta):
        wt = self.wander_target
        jitter_tts = self.wander_jitter * delta
        wt += Vector2D(uniform(-1,1) * jitter_tts, uniform(-1,1) * jitter_tts)
        wt.normalise()
        wt *= self.wander_radius
        target = wt+ Vector2D(self.wander_dist, 0)
        wld_target = self.world.transform_point(target, self.pos.copy(), self.heading, self.side)
        return self.seek(wld_target)

    def avoid_obstacles_force(self):
        detection_box_length = self.min_detection_length + (self.vel.length()/self.max_speed) * self.min_detection_length
        tagged_objects_list = []

        #for obstacle in self.world.obstacles:
            #if (self.pos - obstacle.pos).length() <= detection_box_length:
                #tagged_objects_list.append(obstacle)

        closest_distance = float('inf')
        closest_obstacle = None
        closest_pos = None

        for obstacle in self.world.obstacles:
            local_position = self.world.transform_point(obstacle.pos, self.pos.copy() , self.heading, self.side)
            if local_position.x > 0:
                expanded_radius = obstacle.bounding_radius + self.bRadius
                if abs(local_position.y) < expanded_radius:
                    cX = local_position.x
                    cY = local_position.y

                    sqrt_part = sqrt(expanded_radius**2 - cY**2)

                    ip = cX - sqrt_part
                    if ip < 0.0:
                        ip = cX + sqrt_part
                    if ip < closest_distance:
                        closest_distance = ip
                        closest_obstacle = obstacle
                        closest_pos = obstacle.pos

            steering_force = Vector2D()

            if closest_obstacle:
                multiplier = 1.0 + (detection_box_length - closest_pos.x)/detection_box_length
                steering_force.y = (closest_obstacle.bounding_radius - closest_obstacle.pos.y) * multiplier
                breaking_weight = 0.2 
                steering_force.x = (closest_obstacle.bounding_radius - closest_obstacle.pos.x) * breaking_weight

            return self.world.transform_vector_to_world(steering_force, self.heading, self.side)
        
    def hide(self):
        hunter = self.world.hunter
        distance_to_closest = float('inf')
        best_hiding_spot = None
        best_obstacle = None

        for obstacle in self.world.obstacles:
            obstacle.tagged = False
            hiding_spot = obstacle.get_hiding_position(hunter)
            hiding_distance = self.pos.distance(hiding_spot)               
            if hiding_distance < distance_to_closest:
                distance_to_closest = hiding_distance
                best_hiding_spot = hiding_spot
                best_obstacle = obstacle

        if best_hiding_spot:
            best_obstacle.tagged = True
            return self.arrive(best_hiding_spot, 'fast') 
   
        return self.flee(hunter.pos)

    def switch_weapon(self, weapon_type):
        # Switch the weapon to the type chosen
        self.gun_type = weapon_type
        # Reset the firing timer
        self.firing_timer = 1.0
        # Reset the reload timer
        self.reload_timer = copy(WEAPON_RELOAD_SPEED[weapon_type])

    def separate_from_other(self):
        force = Vector2D()
        agents_list = self.world.target_bots

        for agent in agents_list:
            if agent != self and agent.tagged is True:
                toVector = self.pos - agent.pos
                force += toVector.normalise()/toVector.length()
        
        return force* self.max_force    
    
    def tag_close_enemies(self, radius):
        agents_list = self.world.target_bots
        for agent in agents_list:
            agent.tagged = False
            toVector = self.pos - agent.pos
            gap = radius + agent.bounding_radius
            if toVector.length_sq() < gap**2:
                agent.tagged = True

    def follow_path(self):
        path = self.path
        if path.is_finished():
            return self.arrive(path.current_pt(), 'slow')
        else:
            if (self.pos - path.current_pt()).length() < self.waypoint_threshold:
                path.inc_current_pt()
                self.sub_mode = 'observe'
            return self.seek(path.current_pt())

    def reload(self, delta):
        # Reload the weapon ammunition
        if self.weapon_ammunition_inventory[self.gun_type] < WEAPON_MAX_ROUNDS[self.gun_type]:
            # If the reload timer is not at 0, continue to wait
            if self.reload_timer > 0.0:
                        self.reload_timer -= delta
            # If the reload timer has reached 0
            else:
                # Set the weapon ammo at max capacity (reload)
                self.weapon_ammunition_inventory[self.gun_type] = copy(WEAPON_MAX_ROUNDS[self.gun_type])
                # Reset reload timer
                self.reload_timer = copy(WEAPON_RELOAD_SPEED[self.gun_type])
                # Reset the firing timer
                self.firing_timer = 0.0