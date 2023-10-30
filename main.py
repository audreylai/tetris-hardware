from hardware import *
import time
import math
import random
import pygame
from PIL import Image

cursor_coord = [0, 0]
rotation = 0
next_pieces = []
grid = [[(0, 0, 0) for i in range(10)] for x in range(24)]
floor_pieces = []
hold_piece_key = ""
game_speed = 0.2
level = 0
score = 0

border_color = (10, 10 ,10)

pygame.mixer.init(44100, -16, 1, 512)

tetris_death = pygame.mixer.Sound('./sounds/tetris_death.wav')
tetris_drop = pygame.mixer.Sound('./sounds/tetris_drop.wav')
tetris_level = pygame.mixer.Sound('./sounds/tetris_level.wav')
tetris_oneline = pygame.mixer.Sound('./sounds/tetris_oneline.wav')
tetris_tetris = pygame.mixer.Sound('./sounds/tetris_tetris.wav')

def init_game():
	game_menu()
	draw_rect((0,0), (31, 31), (0,0,0), border=False)
	global next_pieces, cursor_coord, rotation, floor_pieces, grid, hold_piece_key, level, score
	# draw borders
	draw_rect((1, 3), (8, 8), border_color) # hold box
	
	draw_rect((1, 10), (8, 20), border_color) # digits box
	
	draw_rect((10, 3), (21, 28), border_color) # game space
	
	draw_rect((23, 3), (30, 28), border_color) # next
	
	
	cursor_coord = [5, 1]
	rotation = 0
	next_pieces = [str(random.randint(0,6)) for x in range(6)]
	floor_pieces = []
	grid = [[(0, 0, 0) for i in range(10)] for x in range(24)]
	hold_piece_key = ""
	level = 0
	score = 0
	
	for next_p, y_coord in zip(next_pieces, range(6,27,4)):
		draw_piece((26, y_coord), next_p, 0, is_grid=False)

# piece
def get_piece(key, rotation):
	pieces = {
		"0": [
				[0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0],
				[0, 1, 1, 1, 1],
				[0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0]
			],
		"1": [
				[1, 0, 0],
				[1, 1, 1],
				[0, 0, 0]
			],
		"2": [
				[0, 0, 1],
				[1, 1, 1],
				[0, 0, 0]
			],
		"3": [
				[1, 1],
				[1, 1]
			],
		"4": [
				[0, 1, 1],
				[1, 1, 0],
				[0, 0, 0]
			],
		"5": [
				[0, 1, 0],
				[1, 1, 1],
				[0, 0, 0]
			],
		"6": [
				[1, 1, 0],
				[0, 1, 1],
				[0, 0, 0]
			],
	}
	piece = pieces[key]
	for i in range(rotation):
		piece = list(zip(*piece))
		piece = [list(reversed(x)) for x in piece]
	return piece

def get_piece_coord(coord, piece):
	center_y, center_x = math.floor(len(piece)/2), math.floor(len(piece[0])/2)
	piece_coords = []
	for y in range(len(piece)):
		for x in range(len(piece[0])):
			if piece[y][x] == 1:
				piece_coords.append([x + coord[0] - center_x, y + coord[1] - center_y])
	return piece_coords

def draw_piece(coord, key, rotation, undraw=False, is_grid=True, ghost=False):
	global grid
	piece_colors = {
		"0": [x*0.1 for x in (103, 225, 230)],
		"1": [x*0.1 for x in (56, 72, 214)],
		"2": [x*0.1 for x in (222, 163, 44)],
		"3": [x*0.1 for x in (247, 247, 87)],
		"4": [x*0.1 for x in (88, 224, 67)],
		"5": [x*0.1 for x in (161, 38, 209)],
		"6": [x*0.1 for x in (217, 30, 55)]
	}
	piece = get_piece(key, rotation)
	piece_coords = get_piece_coord(coord, piece)
	
	if not undraw:
		for x, y in piece_coords:
			color = piece_colors[key] if not ghost else (1, 1, 1)
			if not is_grid:
				draw(x, y, color)
			else:
				grid[y][x] = color
	else:
		for x, y in piece_coords:
			if not is_grid:
				draw(x, y, (0,0,0))
			else:
				grid[y][x] = (0, 0, 0)


# utility
def is_collide(new_cursor_coord, piece_key, rotation, floor_only=False):
	piece = get_piece(piece_key, rotation)
	piece_coords = get_piece_coord(new_cursor_coord, piece)
	
	if not floor_only:   
		# check wall bounds
		for pc_x, pc_y in piece_coords:
			if pc_x < 0 or pc_x > 9 or pc_y < 0 or pc_y > 23:
				return True
	
	for pc in piece_coords:
		if pc[1] > 23 or pc in floor_pieces:
			return True
	

	return False

def drop_piece(piece_key, rotation):
	pygame.mixer.Sound.play(tetris_drop)
	global floor_pieces, cursor_coord
	while not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation, floor_only=True):
		cursor_coord[1] += 1

def drop_ghost(piece_key, rotation, undraw=False):
	global floor_pieces, cursor_coord
	ghost_coord = cursor_coord.copy()
	while not is_collide((ghost_coord[0], ghost_coord[1]+1), piece_key, rotation, floor_only=True):
		ghost_coord[1] += 1
	draw_piece(ghost_coord, piece_key, rotation, undraw=undraw, ghost=True)

# managment
def manage_next_pieces():
	global next_pieces
	tmp_next = []
	
	draw_rect((24, 4), (29, 27), (0,0,0), border=False)

	if len(tmp_next) == 0:
		tmp_next = random_shuffle([str(x) for x in range(0, 7)])
	
	next_pieces.append(tmp_next.pop(0))
	for next_p, y_coord in zip(next_pieces, range(6,27,4)):
		draw_piece((26, y_coord), next_p, 0, undraw=False, is_grid=False)
	draw_rect((23, 28), (30, 28), border_color)

def swap_hold_piece(new_piece):
	global hold_piece_key, next_pieces

	# swap
	if hold_piece_key == "":
		old_hold_piece_key = next_pieces.pop(0)
	else:
		old_hold_piece_key = hold_piece_key
	
	hold_piece_key = new_piece

	# redraw hold
	draw_rect((1, 3), (8, 8), border_color)
	draw_piece((4, 6), hold_piece_key, 0, is_grid=False)

	return old_hold_piece_key

def manage_level():
	global level, score

	if score > level**2 * 1000:
		pygame.mixer.Sound.play(tetris_level)
		level += 1
	
	if level > 9:
		return True

	numbers = {
		"0": [
			[0, 1, 1, 0],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[0, 1, 1, 0]
		],
		"1": [
			[0, 0, 1, 0],
			[0, 1, 1, 0],
			[1, 0, 1, 0],
			[0, 0, 1, 0],
			[0, 0, 1, 0],
			[0, 0, 1, 0],
			[0, 0, 1, 0]
		],
		"2": [
			[0, 1, 1, 0],
			[1, 0, 0, 1],
			[0, 0, 0, 1],
			[0, 1, 1, 0],
			[1, 0, 0, 0],
			[1, 0, 0, 0],
			[1, 1, 1, 1],
		],
		"3": [
			[0, 1, 1, 0],
			[1, 0, 0, 1],
			[0, 0, 0, 1],
			[0, 1, 1, 0],
			[0, 0, 0, 1],
			[1, 0, 0, 1],
			[0, 1, 1, 0],
		],
		"4": [
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[0, 1, 1, 1],
			[0, 0, 0, 1],
			[0, 0, 0, 1],
			[0, 0, 0, 1],
		],
		"5": [
			[1, 1, 1, 1],
			[1, 0, 0, 0],
			[1, 1, 1, 0],
			[0, 0, 0, 1],
			[0, 0, 0, 1],
			[0, 0, 0, 1],
			[1, 1, 1, 0],
		],
		"6": [
			[0, 1, 1, 0],
			[1, 0, 0, 1],
			[1, 0, 0, 0],
			[1, 1, 1, 0],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[0, 1, 1, 0],
		],
		"7": [
			[1, 1, 1, 1],
			[0, 0, 0, 1],
			[0, 0, 0, 1],
			[0, 0, 1, 0],
			[0, 0, 1, 0],
			[0, 1, 0, 0],
			[0, 1, 0, 0],
		],
		"8": [
			[0, 1, 1, 0],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[0, 1, 1, 0],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[0, 1, 1, 0],
		],
		"9": [
			[0, 1, 1, 0],
			[1, 0, 0, 1],
			[1, 0, 0, 1],
			[0, 1, 1, 1],
			[0, 0, 0, 1],
			[1, 0, 0, 1],
			[0, 1, 1, 0],
		]
	}
	number = numbers[str(level)]
	for x in range(0, len(number[0])):
		for y in range(len(number)):
			number_color = (36, 70, 87) if number[y][x] == 1 else (0,0,0)
			draw(x+3, y+12, color=number_color)

# check functions
def check_is_full():
	global floor_pieces
	return any([True for fp in floor_pieces if fp[1] < 1])

def check_clear_lines():
	global floor_pieces, score, level
	n_clears = 0
	for y in range(24):
		if len([fp for fp in floor_pieces if fp[1] == y]) == 10:
			n_clears += 1
			floor_pieces = [fp for fp in floor_pieces if fp[1] != y]
			for i in range(len(floor_pieces)):
				if floor_pieces[i][1] < y:
					floor_pieces[i][1] += 1
			grid.pop(y)
			grid.insert(0, [(0,0,0) for abc in range(10)])
	if n_clears == 4:
		pygame.mixer.Sound.play(tetris_tetris)
		score += 800 * level
	elif n_clears > 0:
		pygame.mixer.Sound.play(tetris_oneline)
		score += n_clears*100 + (n_clears-1)*100

def game_loop():
	global rotation, cursor_coord, next_pieces, floor_pieces, game_speed, score
	can_move = False
	already_hold = False

	# timers
	rotation_timer = time.time()
	drop_timer = time.time()
	move_timer = time.time()
	joystick_timer = time.time()
	check_timer = time.time()

	piece_key = None
	while True:
		if get_button_press("start") or check_is_full() or manage_level():
			pygame.mixer.Sound.play(tetris_death)
			init_game()
			can_move = False
		if not can_move:
			piece_key = next_pieces.pop(0)
			rotation = 0
			cursor_coord = [5, 1]
			manage_next_pieces()
			can_move = True

		check_clear_lines()
		drop_ghost(piece_key, rotation, undraw=True)
		draw_piece(cursor_coord, piece_key, rotation, undraw=True)

		# joystick controls
		if time.time() - joystick_timer > 0.09:
			if joystick_moved("left") and not is_collide((cursor_coord[0]-1, cursor_coord[1]), piece_key, rotation):
				cursor_coord[0]-=1
				joystick_timer = time.time()
			if joystick_moved("right") and not is_collide((cursor_coord[0]+1, cursor_coord[1]), piece_key, rotation):
				cursor_coord[0]+=1
				joystick_timer = time.time()
			if joystick_moved("down") and not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation):
				game_speed = 0.01
				joystick_timer = time.time()
			else:
				game_speed = 0.2
		
		if get_button_press("rotate") and (time.time() - rotation_timer > 0.2):
			if is_collide(cursor_coord, piece_key, rotation + 1):
				print(cursor_coord)
				if cursor_coord[0] < 5:
					cursor_coord = [cursor_coord[0]+1, cursor_coord[1]]
				else:
					cursor_coord = [cursor_coord[0]-1, cursor_coord[1]]
					# pass
			rotation += 1

			rotation_timer = time.time()

		if get_button_press("hold") and not already_hold:
			piece_key = swap_hold_piece(piece_key)
			rotation = 0
			cursor_coord = [5, 1]
			manage_next_pieces()
			already_hold = True
		if get_button_press("drop") and (time.time() - drop_timer > 0.2):
			drop_piece(piece_key, rotation)
			drop_timer = time.time()
			check_timer = 1
		
		# moving down / gravity
		if not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation, floor_only=True):
			if (time.time() - move_timer > game_speed):
				cursor_coord[1] += 1
				move_timer = time.time()
			check_timer = time.time()
		elif (time.time() - check_timer > 0.5):
			for c in get_piece_coord((cursor_coord[0], cursor_coord[1]), get_piece(piece_key, rotation)):
				floor_pieces.append(c)
			can_move = False
			already_hold = False
		
		drop_ghost(piece_key, rotation)
		draw_piece(cursor_coord, piece_key, rotation)

		if rotation > 3:
			rotation = 0

		draw_grid(grid)
		pixels.show()

def game_menu():
	draw_rect((0,0), (31, 31), (0,0,0), border=False)
	pixels.show()

	in_menu = True
	while in_menu:
		if get_button_press("rotate"):
			in_menu = False
		
		img = Image.open("menu.png")
		from numpy import array
		arr = array(img)
		
		for y in range(0, 32):
			for x in range(0, 32):
				# print(arr[y][x])
				draw(x, y, arr[y][x][:3]*0.05)
		pixels.show()
		



if __name__ == "__main__":
	# game_menu()
	init_game()
	pixels.show()
	game_loop()
