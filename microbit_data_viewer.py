import pygame
import csv
import random

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
def getRandomColor(): return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

SCREENSIZE = [700, 700]
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 50)
FONTHEIGHT = FONT.render("0", True, BLACK).get_height()

f = []
with open('microbit_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader:
		f.append(row)
headers = f[0]
values = f[1:]

numValues = len(values)
maxValue = 0
for frame in range(len(values)):
		for data_type in range(len(headers)):
			value = int(values[frame][data_type])
			maxValue = max(value, maxValue)

colors = []
for r in [0, 128, 255]:
	for g in [0, 128, 255]:
		for b in [0, 128, 255]:
			colors.append((r, g, b))
colors.remove((0, 0, 0))
colors.remove((255, 255, 255))
random.shuffle(colors)

zoomX = 50
zoomY = 0.5
SCREENSIZE = [numValues * zoomX, (maxValue * zoomY) + FONTHEIGHT]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.VIDEORESIZE:
			zoomX = event.dict["size"][0] / numValues
			zoomY = (event.dict["size"][1] - FONTHEIGHT) / maxValue
			SCREENSIZE = [event.dict["size"][0], event.dict["size"][1]]
			screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
	screen.fill(WHITE)
	for frame in range(len(values)):
		for data_type in range(len(headers)):
			value = int(values[frame][data_type])
			pygame.draw.circle(screen, colors[data_type], (frame * zoomX, SCREENSIZE[1] - (value * zoomY)), 10)
			try:
				next_value = int(values[frame + 1][data_type])
				pygame.draw.line(screen, colors[data_type], (frame * zoomX, SCREENSIZE[1] - (value * zoomY)), ((frame + 1) * zoomX, SCREENSIZE[1] - (next_value * zoomY)), 1)
			except: None;
	# HEADER
	pos = pygame.mouse.get_pos()
	p = 0
	pygame.draw.rect(screen, GRAY, pygame.Rect(0, 0, SCREENSIZE[0], FONTHEIGHT))
	screen.blit(FONT.render(f"Micro:bit Data", True, BLACK), (0, 0))
	for frame in range(len(values)):
		for data_type in range(len(headers)):
			value = int(values[frame][data_type])
			r = pygame.Rect((frame * zoomX) - 10, (SCREENSIZE[1] - (value * zoomY)) - 10, 20, 20)
			if r.collidepoint(*pos):
				p += FONTHEIGHT
				pygame.draw.rect(screen, GRAY, pygame.Rect(0, p, SCREENSIZE[0], FONTHEIGHT))
				pygame.draw.rect(screen, colors[data_type], pygame.Rect(0, p, SCREENSIZE[0], FONTHEIGHT), 3)
				screen.blit(FONT.render(f"{headers[data_type]} at {frame} is: {value}", True, BLACK), (0, p))
	pygame.display.flip()
pygame.quit()
