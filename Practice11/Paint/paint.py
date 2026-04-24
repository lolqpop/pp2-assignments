import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    radius = 2
    # Tools: brush, rect, circle, eraser, square, r_tri, e_tri, rhombus
    tool = 'brush' 
    colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 255), (255, 255, 0)]
    color_index = 0
    
    objects = []
    current_shape_start = None
    drawing = False

    while True:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                # Tool choice
                if event.key == pygame.K_1: tool = 'brush'
                elif event.key == pygame.K_2: tool = 'rectangle'
                elif event.key == pygame.K_3: tool = 'circle'
                elif event.key == pygame.K_4: tool = 'eraser'
                elif event.key == pygame.K_5: color_index = (color_index + 1) % len(colors)
                elif event.key == pygame.K_6: tool = 'square'
                elif event.key == pygame.K_7: tool = 'r_triangle' 
                elif event.key == pygame.K_8: tool = 'e_triangle' 
                elif event.key == pygame.K_9: tool = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    current_shape_start = event.pos
                    active_color = (0, 0, 0) if tool == 'eraser' else colors[color_index]
                    if tool in ['brush', 'eraser']:
                        objects.append({'type': 'line', 'points': [event.pos], 'color': active_color, 'radius': radius})
                
                elif event.button == 4: radius = min(100, radius + 1)
                elif event.button == 5: radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    active_color = (0, 0, 0) if tool == 'eraser' else colors[color_index]
                    if tool not in ['brush', 'eraser']:
                        objects.append({'type': tool, 'start': current_shape_start, 'end': event.pos, 'color': active_color, 'radius': radius})
                    drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool in ['brush', 'eraser']:
                    objects[-1]['points'].append(event.pos)

        # Rendering all objects
        for obj in objects:
            draw_object(screen, obj)
        
        # Preview of current figure
        if drawing and current_shape_start and tool not in ['brush', 'eraser']:
            active_color = (0, 0, 0) if tool == 'eraser' else colors[color_index]
            temp_obj = {'type': tool, 'start': current_shape_start, 'end': pygame.mouse.get_pos(), 'color': active_color, 'radius': radius}
            draw_object(screen, temp_obj)

        display_info(screen, tool, colors[color_index], radius)
        pygame.display.flip()
        clock.tick(60)

def draw_object(screen, obj):
    color, start, end, rad = obj.get('color'), obj.get('start'), obj.get('end'), obj.get('radius', 1)
    
    if obj['type'] == 'line':
        for i in range(len(obj['points']) - 1):
            pygame.draw.line(screen, obj['color'], obj['points'][i], obj['points'][i+1], obj['radius'] * 2)
            pygame.draw.circle(screen, obj['color'], obj['points'][i], obj['radius'])

    elif obj['type'] == 'rectangle':
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), abs(start[0]-end[0]), abs(start[1]-end[1]))
        pygame.draw.rect(screen, color, rect, rad)

    elif obj['type'] == 'square':
        side = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
        s_x = start[0] if end[0] > start[0] else start[0] - side
        s_y = start[1] if end[1] > start[1] else start[1] - side
        pygame.draw.rect(screen, color, (s_x, s_y, side, side), rad)

    elif obj['type'] == 'circle':
        dist = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
        pygame.draw.circle(screen, color, start, dist, rad)

    elif obj['type'] == 'r_triangle': # Right Triangle 
        points = [start, (start[0], end[1]), end]
        pygame.draw.polygon(screen, color, points, rad)

    elif obj['type'] == 'e_triangle': # Equilateral 
        height = end[1] - start[1]
        width = (end[0] - start[0])
        points = [(start[0] + width//2, start[1]), (start[0], end[1]), (end[0], end[1])]
        pygame.draw.polygon(screen, color, points, rad)

    elif obj['type'] == 'rhombus': # Rhombus 
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        points = [(mid_x, start[1]), (end[0], mid_y), (mid_x, end[1]), (start[0], mid_y)]
        pygame.draw.polygon(screen, color, points, rad)

def display_info(screen, tool, color, radius):
    font = pygame.font.SysFont("Arial", 16)
    txt = f"Tool: {tool} | Radius: {radius} | 1-4: Basic | 6: Sq | 7: R-Tri | 8: E-Tri | 9: Rhomb"
    img = font.render(txt, True, (255, 255, 255))
    screen.blit(img, (10, 10))
    pygame.draw.rect(screen, color, (10, 30, 20, 20))

main()