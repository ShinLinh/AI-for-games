# variables:
# enemy HP
HP = 100
# enemy position
sPosX = 10
sPosY = 10
# enemy movement speed
movSpeedHorizontal = 5
movSpeedVertical = 2
#player position
playerPosX = 100
playerPosY = 100
# attack range of the enemy
attack_range = 3
#whether the enemy is alive or not
alive  = True

# list of states
states = ['patrolling', 'engaging', 'dying']
#list of substates
substates = ['approaching', 'attacking', 'none']
# current state of the enemy
current_state = 'patrolling'
# current substate of the enemy's state
current_substate = 'none'


while alive:
	# check if the enemy's HP has reached 0
	if HP <= 0:
		#switch the state of the enemy to 'dying' to run death scripts 
		current_state = 'dying'
		
	# clear the substate if the current state is not 'engaging', as at this point only 'engaging' has a substate
	if current_state is not 'engaging'
		current_substate = 'none'
		
	# Handle state switching from the patrolling state
	if current_state is 'patrolling':
		# check if the the player is on the enemy line of sight, which is a horizontal line 6 units in height, and infinite length
		if playerPosY > sPosY - 3 and playerPosY < sPosY + 3:
			# switch to the 'engaging' state
			current_state = 'engaging'
			
	# check if the current state is 'patrolling', when the enemy has not found the player
	if current_state is 'patrolling':
		# move the enemy in a preset pattern and area using the horizontal and vertical movespeed values.
		if sPosX > 100:
			if sPosX > 10:
				sPosX -= movSpeedHorizontal
		if sPosX < 10:
			if sPosX < 100:
				sPosX += movSpeedHorizontal
		if sPosY > 100:
			if sPosY > 10:
				sPosY -= movSpeedVertical
		if sPosY < 10:
			if sPosY < 100:
				sPosY += movSpeedVertical
				
	# handle substate switching during the engaging state:
	if current_state is 'engaging':
		# calculate the distance between the player and the enemy
		distance = math.sqrt(math.pow(playerPosX- sPosX, 2) + math.pow(playerPosY - sPosY))
		
		# check if the attacking animation is playing
		if not attacking():
			# check if the player is within attack range
			if distance <= attack_range:
				# change the substate to 'attacking' so that the enemy starts attacking the player
				current_substate = 'attacking'
			else
				# change the substate to 'approaching' so that the enemy tries to get close to the player
				current_substate = 'approaching' 
				
	# check if the current state is 'engaging', when the enemy has found the player
	if current_state is 'engaging':
		if current_substate = 'attacking'
			# run the script for attacking the player
			attack_player()
		if current_substate = 'appproaching'
			# run the script for getting close to the player
			move_toward_player()
			
	# check if the current state is 'dying', when the enemy HP reaches 0
	if current_state = 'dying'
		#check whether the death animation has finished
		if death_animation_done():
			# if the death animation has finished, change the enemy's alive value to false to terminate the loop
			alive = False
		else # if the animation is not finished yet.
			# check if the death animation is not playing
			if not playing_death_animation():
				# play death animation
				play_death_animation()
		
		
			
		
		

