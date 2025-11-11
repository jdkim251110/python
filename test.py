"""
Simple Tetris implemented with pygame.

Controls (focus the game window):
  Left / Right Arrow : move piece
  Up Arrow           : rotate piece
  Down Arrow         : soft drop
  Space              : hard drop
  P                  : pause
  Esc / Q            : quit

Run: python test.py

Dependencies: pygame
"""

import sys
import random
import pygame

# Game settings
CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE * ROWS
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
COLORS = [
	(0, 240, 240),  # I
	(0, 0, 240),    # J
	(240, 160, 0),  # L
	(240, 240, 0),  # O
	(0, 240, 0),    # S
	(160, 0, 240),  # T
	(240, 0, 0),    # Z
]

# Tetromino definitions: each shape is a list of rotation states (matrix)
TETROMINOS = {
	'I': [
		[[1,1,1,1]],
		[[1],[1],[1],[1]],
	],
	'J': [
		[[1,0,0],[1,1,1]],
		[[1,1],[1,0],[1,0]],
		[[1,1,1],[0,0,1]],
		[[0,1],[0,1],[1,1]],
	],
	'L': [
		[[0,0,1],[1,1,1]],
		[[1,0],[1,0],[1,1]],
		[[1,1,1],[1,0,0]],
		[[1,1],[0,1],[0,1]],
	],
	'O': [
		[[1,1],[1,1]],
	],
	'S': [
		[[0,1,1],[1,1,0]],
		[[1,0],[1,1],[0,1]],
	],
	'T': [
		[[0,1,0],[1,1,1]],
		[[1,0],[1,1],[1,0]],
		[[1,1,1],[0,1,0]],
		[[0,1],[1,1],[0,1]],
	],
	'Z': [
		[[1,1,0],[0,1,1]],
		[[0,1],[1,1],[1,0]],
	],
}

SHAPE_NAMES = list(TETROMINOS.keys())


class Piece:
	def __init__(self, name=None):
		self.name = name or random.choice(SHAPE_NAMES)
		self.states = TETROMINOS[self.name]
		self.state = 0
		self.matrix = self.states[self.state]
		self.color = COLORS[SHAPE_NAMES.index(self.name)]
		# spawn near top center
		self.x = COLUMNS // 2 - len(self.matrix[0]) // 2
		self.y = 0

	def rotate(self, grid):
		old_state = self.state
		self.state = (self.state + 1) % len(self.states)
		self.matrix = self.states[self.state]
		if self._collide(grid):
			# try wall kicks horizontally
			for dx in (-1, 1, -2, 2):
				self.x += dx
				if not self._collide(grid):
					return True
				self.x -= dx
			# revert
			self.state = old_state
			self.matrix = self.states[self.state]
			return False
		return True

	def _collide(self, grid, dx=0, dy=0):
		for r, row in enumerate(self.matrix):
			for c, val in enumerate(row):
				if not val:
					continue
				gx = self.x + c + dx
				gy = self.y + r + dy
				if gx < 0 or gx >= COLUMNS or gy >= ROWS:
					return True
				if gy >= 0 and grid[gy][gx] is not None:
					return True
		return False

	def move(self, dx, dy, grid):
		if not self._collide(grid, dx, dy):
			self.x += dx
			self.y += dy
			return True
		return False

	def hard_drop(self, grid):
		while not self._collide(grid, 0, 1):
			self.y += 1

	def lock(self, grid):
		for r, row in enumerate(self.matrix):
			for c, val in enumerate(row):
				if not val:
					continue
				gx = self.x + c
				gy = self.y + r
				if 0 <= gy < ROWS and 0 <= gx < COLUMNS:
					grid[gy][gx] = self.color


def create_grid():
	return [[None for _ in range(COLUMNS)] for _ in range(ROWS)]


def clear_lines(grid):
	new_grid = [row for row in grid if any(cell is None for cell in row)]
	lines_cleared = ROWS - len(new_grid)
	if lines_cleared:
		for _ in range(lines_cleared):
			new_grid.insert(0, [None for _ in range(COLUMNS)])
	return new_grid, lines_cleared


def draw_grid(surface):
	for x in range(COLUMNS + 1):
		pygame.draw.line(surface, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
	for y in range(ROWS + 1):
		pygame.draw.line(surface, GRAY, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))


def draw_playfield(surface, grid):
	for r in range(ROWS):
		for c in range(COLUMNS):
			cell = grid[r][c]
			rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			if cell is not None:
				pygame.draw.rect(surface, cell, rect)
				pygame.draw.rect(surface, BLACK, rect, 1)
			else:
				pygame.draw.rect(surface, BLACK, rect, 1)


def draw_piece(surface, piece):
	for r, row in enumerate(piece.matrix):
		for c, val in enumerate(row):
			if not val:
				continue
			x = (piece.x + c) * CELL_SIZE
			y = (piece.y + r) * CELL_SIZE
			rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(surface, piece.color, rect)
			pygame.draw.rect(surface, BLACK, rect, 1)


def draw_side_panel(surface, next_piece, score, level):
	font = pygame.font.SysFont('Arial', 20)
	x = WIDTH + 10
	surface.fill((10, 10, 10), pygame.Rect(WIDTH, 0, 200, HEIGHT))
	lbl = font.render(f'Score: {score}', True, WHITE)
	surface.blit(lbl, (x, 10))
	lbl2 = font.render(f'Level: {level}', True, WHITE)
	surface.blit(lbl2, (x, 40))
	lbl3 = font.render('Next:', True, WHITE)
	surface.blit(lbl3, (x, 80))
	# draw next piece scaled
	for r, row in enumerate(next_piece.matrix):
		for c, val in enumerate(row):
			if not val:
				continue
			rect = pygame.Rect(x + c * CELL_SIZE, 110 + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(surface, next_piece.color, rect)
			pygame.draw.rect(surface, BLACK, rect, 1)


def main():
	pygame.init()
	pygame.display.set_caption('Tetris')
	screen = pygame.display.set_mode((WIDTH + 200, HEIGHT))
	clock = pygame.time.Clock()

	grid = create_grid()
	current = Piece()
	next_piece = Piece()
	score = 0
	level = 1
	lines = 0

	fall_time = 0
	fall_speed = 0.8  # seconds per cell at level 1
	running = True
	paused = False

	while running:
		dt = clock.tick(FPS) / 1000.0
		if not paused:
			fall_time += dt

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					running = False
				if event.key == pygame.K_p:
					paused = not paused
				if not paused:
					if event.key == pygame.K_LEFT:
						current.move(-1, 0, grid)
					elif event.key == pygame.K_RIGHT:
						current.move(1, 0, grid)
					elif event.key == pygame.K_DOWN:
						if current.move(0, 1, grid):
							score += 1
					elif event.key == pygame.K_UP:
						current.rotate(grid)
					elif event.key == pygame.K_SPACE:
						current.hard_drop(grid)
						# after hard drop, lock
						current.lock(grid)
						grid, cleared = clear_lines(grid)
						if cleared:
							lines += cleared
							score += 100 * (2 ** (cleared - 1))
						current = next_piece
						next_piece = Piece()
						# if new piece collides immediately -> game over
						if current._collide(grid):
							running = False

		# automatic fall
		if not paused and fall_time > max(0.05, fall_speed - (level - 1) * 0.05):
			fall_time = 0
			if not current.move(0, 1, grid):
				# lock piece
				current.lock(grid)
				grid, cleared = clear_lines(grid)
				if cleared:
					lines += cleared
					score += 100 * (2 ** (cleared - 1))
					level = 1 + lines // 10
				current = next_piece
				next_piece = Piece()
				if current._collide(grid):
					running = False

		# draw
		screen.fill(BLACK)
		play_surface = screen.subsurface((0, 0, WIDTH, HEIGHT))
		play_surface.fill((5, 5, 5))
		draw_playfield(play_surface, grid)
		draw_piece(play_surface, current)
		draw_grid(play_surface)

		# side panel
		side_surface = screen.subsurface((WIDTH, 0, 200, HEIGHT))
		draw_side_panel(screen, next_piece, score, level)

		if paused:
			font = pygame.font.SysFont('Arial', 40)
			txt = font.render('PAUSED', True, WHITE)
			screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - txt.get_height() // 2))

		pygame.display.flip()

	# game over screen
	font = pygame.font.SysFont('Arial', 40)
	screen.fill(BLACK)
	txt = font.render('GAME OVER', True, WHITE)
	screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - txt.get_height() // 2))
	small = pygame.font.SysFont('Arial', 24).render(f'Score: {score}', True, WHITE)
	screen.blit(small, (WIDTH // 2 - small.get_width() // 2, HEIGHT // 2 + 40))
	pygame.display.flip()
	pygame.time.wait(3000)
	pygame.quit()


if __name__ == '__main__':
	main()



