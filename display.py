import pygame
import simul
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("nBody Simulation")

clock = pygame.time.Clock()

system = simul.Simulation()
#system = simul.Simulation(3, (50, 50, 0.00015), [[50,0], [-50, 0], [200, 0]], [[0, -1], [0, 1], [0, 2]])
#system = simul.Simulation(nPlanets = 4, planetMasses = (25.,25.,25., 25.), planetPositions = [[100,0], [-100,0], [0,100], [0,-100]], startingVelocities= [[0,-1], [0,1], [1,0], [-1,0]])
#system = simul.Simulation(planetPositions=[[float(random.randint(-200, -200)), float(random.randint(-200, 200))] for _ in range(3)], startingVelocities=[[random.uniform(-1,1),random.uniform(-1,1)] for _ in range(3)])

running = True

def center_origin(surf, p):
    return ((p[0]*zoomFactor) + movingOffset[0] + surf.get_width() // 2, (p[1]*zoomFactor) + movingOffset[1] + surf.get_height() // 2)

storedOffset = [0,0]
movingOffset = [0,0]

zoomFactor = 1.
zoomSens = 0.1

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            downPos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            storedOffset = movingOffset[:]
            
        if event.type == pygame.MOUSEWHEEL:  # Detect scrolling
            zoomFactor *= 1 + (event.y * zoomSens)  # Increase/decrease zoom
            zoomFactor = max(0.1, min(5.0, zoomFactor)) 
    
    buttons = pygame.mouse.get_pressed()
    if buttons[0]:  # Left mouse button
        currentPos = pygame.mouse.get_pos()
        movingOffset[0] = currentPos[0]-downPos[0] + storedOffset[0]
        movingOffset[1] = currentPos[1]-downPos[1] + storedOffset[1]


    screen.fill(BLACK)
    
    for planet in system.planets:
        trail_length = len(planet.trail)
        fade_count = min(50, trail_length)


        trail_points = []
        
        for i, point in enumerate(planet.trail):
            if i < fade_count: 
                fade_factor = i / fade_count
                color = (
                    int(planet.col[0] * fade_factor), 
                    int(planet.col[1] * fade_factor), 
                    int(planet.col[2] * fade_factor)
                ) 
            else:
                color = planet.col
            
            trail_points.append((point, color))

        for i in range(1, len(trail_points)):
            start_point, start_color = trail_points[i-1]
            end_point, end_color = trail_points[i]
        
            pygame.draw.line(screen, start_color, center_origin(screen, start_point), center_origin(screen, end_point), 1)
            
    for planet in system.planets:
        pygame.draw.circle(screen, planet.col, center_origin(screen, planet.pos), planet.size*zoomFactor)


    pygame.display.flip()

    system.update()

    clock.tick(FPS)

pygame.quit()