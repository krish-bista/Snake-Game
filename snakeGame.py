import pygame
import random
import os
import time


def home_screen():
	# bgSound = pygame.mixer.Sound('background.mp3')
	# pygame.mixer.Channel(0).play(bgSound)
	exitGame = False
	while not exitGame:
		gameWindow.fill(black)
		pygame.draw.rect(gameWindow, blue, [246, 248, 370, 40])
		text_screen("Welcome to Snakes", white, 250, 250)
		text_screen("Press SpaceBar to play", green, 220, 320)
		pygame.draw.line(gameWindow, pink, [215, 366], [645, 366])	

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_loop()

		pygame.display.update()
		clock.tick(50)


def text_screen(text, color, x, y):
	"""
	This function is to display given string in the game window
	by giving its content, color, x-cordinates and y-cordinates
	"""
	pygame.font.init()
	font = pygame.font.SysFont(None, 55, bold=False, italic=False)
	textSc = font.render(text, True, color)
	gameWindow.blit(textSc, [x, y])

def pause():
	paused = True
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					paused = False

		gameWindow.fill(black)
		text_screen("Paused", green, 250, 250)
		text_screen("Press Esc key again to resume", green, 250, 300)
		pygame.display.update()

def quit_game():
	pygame.quit()
	exit()	


def plot_snake(gameWindow, color, snakeList, snakeSize):
	"""
	This function will check snakeList and make rectangles on the
	screen in given coordinates of snakeList to form a snake
	"""
	for x, y in snakeList:
		pygame.draw.rect(gameWindow, color, [x, y, snakeSize, snakeSize])


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 0, 100)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (33,22, 229)


# Some more additional variables
gameHeight = 600
gameWidth = 900
clock = pygame.time.Clock()


# Initializing stuff and creating game window
pygame.init()
pygame.mixer.init()
gameWindow = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Snake Game ~ By Krish Bista")

# Gameloop
def game_loop():
	# Game specific Variables
	exitGame = False
	gameOver = False
	snakeX = random.randint(50, gameWidth-10)
	snakeY = random.randint(50, 300)
	snakeSize = 20
	velocityX = 0
	velocityY = 0
	fps = 50
	foodX = random.randint(10, 850)
	foodY = random.randint(60, 535)
	score = 0
	snakeList = []
	snakeLength = 1


	# Checking current high score or placing 0 if playing first time
	if not os.path.exists("highScore.txt"):
		with open("highScore.txt", "w") as f:
			f.write('0')

	with open("highScore.txt", "r") as f:
		highScore = f.read()
		if highScore == '':
			with open("highScore.txt", "w") as k:
				k.write('0')
	
	# Game starts here
	while True:	

		# Code if its game over
		if gameOver:
			# Writing highscore in a txt file
			
			with open("highScore.txt", "w") as f:
				f.write(str(highScore))
	
			gameWindow.fill(black)
			text_screen("Game Over Press Enter to continue", green, 120, 250)
			text_screen("Score: " + str(score), blue, 350, 320)		
			# Handling events while in game over screen
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit_game()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						gameOver = False
						home_screen()


		# Code if the user is still playing

		else:
			# Handling event while game is on
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit_game()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						velocityX = 5
						velocityY = 0

					elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
						velocityX = -5
						velocityY = 0

					elif event.key == pygame.K_UP or event.key == pygame.K_w:
						velocityY = -5
						velocityX = 0

					elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
						velocityY = 5
						velocityX = 0

					elif event.key == pygame.K_ESCAPE:
						pause()

			# Moving the snake
			snakeX = snakeX + velocityX
			snakeY = snakeY + velocityY

			gameWindow.fill(black)


			# Increasing length of snake and score if the snake eats the food
			if abs(snakeX - foodX) < 15 and abs(snakeY - foodY) < 15:
				beepSound = pygame.mixer.Sound('beep.mp3')
				pygame.mixer.Channel(1).play(beepSound)
				foodX = random.randint(10, 850)
				foodY = random.randint(60, 535)
				score += 10
				snakeLength += 5

			text_screen("Score: " + str(score) + "      HighScore: " + str(highScore), white, 5, gameHeight-45)
			text_screen("Snake Game -- By Krish Bista", white, 200, 5)


			# Updating the coordinates of head and adding in snakeList which results
			# in the increase in length of snake
			head = []
			head.append(snakeX)
			head.append(snakeY)
			snakeList.append(head)


			if len(snakeList) > snakeLength:
				del snakeList[0]


			# Making game over if the snake goes beyond the game playing area
			if snakeX < 0 or snakeX > gameWidth or snakeY < 50 or snakeY > 530:
				gameOverSound = pygame.mixer.Sound('gameOver.mp3')
				pygame.mixer.Channel(0).play(gameOverSound)
				gameOver = True


			# Making game over if the snake head goes into its body
			if head in snakeList[:-1]:
				gameOverSound = pygame.mixer.Sound('gameOver.mp3')
				pygame.mixer.Channel(0).play(gameOverSound)
				gameOver = True


			# Updating highscore if current score is greater than highscore
			if score > int(highScore):
				highScore = score
				

			# Putting severeal game items in game window
			plot_snake(gameWindow, green, snakeList, snakeSize)
			pygame.draw.line(gameWindow, red, [2, 50], [gameWidth, 50])
			pygame.draw.line(gameWindow, red, [0, gameHeight-55], [gameWidth, gameHeight-55])
			pygame.draw.circle(gameWindow, pink, [foodX, foodY], 8)
		
		pygame.display.update()
		clock.tick(fps)	


home_screen()
