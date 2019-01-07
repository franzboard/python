#!/usr/bin/python3
import pgzrun
from gpiozero import Button, LED
import random

WIDTH = 1200
HEIGHT = 1000
PIN_LEFT = 22
PIN_MISSILE = 27
PIN_RIGHT = 17
PIN_LED1 = 18
PIN_LED2 = 23
PIN_LED3 = 24
PIN_LED4 = 25
button_left = Button(PIN_LEFT)
button_missile = Button(PIN_MISSILE)
button_right = Button(PIN_RIGHT)

# The Launcher
launcher = Actor('launcher')
launcher.pos = int(WIDTH/2),HEIGHT-50
launcher_speed = 5

# The Asteroid
ASTEROID_SIZE = 50,46
asteroid = Actor('asteroid')
asteroid.pos = (random.randint(ASTEROID_SIZE[0]/2, WIDTH-(ASTEROID_SIZE[0]/2)),ASTEROID_SIZE[1])
asteroid_speed = 1

# The missile
MISSILE_SIZE = 20,43
missile = Actor('missile')
# initially set missile position in top corner
missile.pos = 0,0
missile_speed = 10
# Status 0 = not fired, 1 = fired
missile_status = 0

# The LED output
led1 = LED(PIN_LED1)
led2 = LED(PIN_LED2)
led3 = LED(PIN_LED3)
led4 = LED(PIN_LED4)
# Status 0 = stop, 1 = playing game
game_status = 0
game_score = 0
def draw():
	if game_status == 0:
		screen.draw.text("Press ENTER to start", (100, 300),
		color="white", fontsize=32)
	if game_status == 1:

		screen.clear()
		# display score
		screen.draw.text("Score: " + str(game_score), (WIDTH-100, 50),
		color="blue", fontsize=24)
		launcher.draw()
		# Each draw loop move asteroid down 1 position
		move_asteroid()
		asteroid.draw()
		# If missile launched move missile up and show
		if missile_status > 0 :
			move_missile()
			missile.draw()
		# Detect if missile / asteroid has hit etc
		detect_hits()

def update():
	global game_status, game_score, missile_status, asteroid_speed
	if game_status == 0:
		if keyboard.RETURN:
			game_status = 1
			asteroid.pos = (random.randint(ASTEROID_SIZE[0]/2, WIDTH-(ASTEROID_SIZE[0]/2)),
			ASTEROID_SIZE[1])
			game_score = 0
			asteroid_speed = 1
	elif game_status == 1:
		# Keyboard movement
		if keyboard.right or button_right.is_pressed :
			move_launcher(launcher_speed)
		if keyboard.left or button_left.is_pressed :
			move_launcher(-1 * launcher_speed)
			
		# If missile not fired then it can be fired
		if missile_status == 0:
			if keyboard.space or button_missile.is_pressed :
				# set position to location of launcher
				missile.pos = (launcher.x, HEIGHT - 50)
				# set it fired
				missile_status = 1
					
# Move launcher allowing, prevent overrunning
def move_launcher(distance):
	newpos = launcher.x + distance
	if (newpos < 50):
		newpos = 50
	elif (newpos > WIDTH-50):
		newpos = WIDTH-50
	launcher.x = newpos
	
# Move asteroid position and check for hits
def move_asteroid():
	global game_status
	# Move position down
	asteroid.pos = (asteroid.x, asteroid.y+asteroid_speed)

# If missile launched then move it up appropriate distance
def move_missile():
	global missile_status
	# Only move / draw if missile is fired
	if missile_status > 0:
		missile.pos = (missile.x, missile.y - missile_speed)
	# Near top and not collided so stop missile
		if missile.y < 10:
			missile_status = 0
			
			
# Check for hits between asteroid and ground / missile
def detect_hits():
	global game_status, game_score, missile_status, asteroid_speed
	# Check if we have hit the ground (game over)
	if asteroid.y >= HEIGHT-(ASTEROID_SIZE[1]/2):
		screen.draw.text("Game Over", (100, 100), color="red", fontsize=32)
		# Stop the game
		game_status = 0
		
	# check if missile has hit asteroid
	if missile_status == 1 and asteroid.collidepoint(missile.pos):
		# When hit asteroid add point and start new
		hit_asteroid()
		missile_status = 0
		# increase asteroid_speed
		asteroid_speed += 1
		game_score += 1
		
def leds_on():
	led1.on()
	led2.on()
	led3.on()
	led4.on()
	
def leds_off():
	led1.off()
	led2.off()
	led3.off()
	led4.off()

# When hit reset the asteroid position
def hit_asteroid():
	# Set new position
	asteroid.pos = (random.randint(ASTEROID_SIZE[0]/2, WIDTH-(ASTEROID_SIZE[0]/2)),ASTEROID_SIZE[1])
	leds_on()
	clock.schedule_unique(leds_off, 0.5)
	
pgzrun.go()
