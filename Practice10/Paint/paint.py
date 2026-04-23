import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    radius = 15
    tool = 'brush' # Modes: 'brush', 'rectangle', 'circle', 'eraser'
    
    # Список доступных цветов для циклического переключения
    colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 255), (255, 255, 0)]
    color_index = 0 # Текущий выбранный индекс цвета
    
    objects = []
    current_shape_start = None
    drawing = False

    while True:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                
                # Color choice
                if event.key == pygame.K_r: color_index = 1 # Red
                elif event.key == pygame.K_g: color_index = 2 # Green
                elif event.key == pygame.K_b: color_index = 0 # Blue
                
                # Key 5 shifts a color 
                elif event.key == pygame.K_5:
                    color_index = (color_index + 1) % len(colors)
                
                # Tool choice
                if event.key == pygame.K_1: tool = 'brush'
                if event.key == pygame.K_2: tool = 'rectangle'
                if event.key == pygame.K_3: tool = 'circle'
                if event.key == pygame.K_4: tool = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Левый клик
                    drawing = True
                    current_shape_start = event.pos
                    # Получаем текущий цвет (черный если ластик, иначе из списка)
                    active_color = (0, 0, 0) if tool == 'eraser' else colors[color_index]
                    
                    if tool == 'brush' or tool == 'eraser':
                        objects.append({
                            'type': 'line', 
                            'points': [event.pos], 
                            'color': active_color, 
                            'radius': radius
                        })
                
                # Size changing (mouse wheel)
                elif event.button == 4: radius = min(200, radius + 2)
                elif event.button == 5: radius = max(1, radius - 2)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if tool == 'rectangle' or tool == 'circle':
                        active_color = (0, 0, 0) if tool == 'eraser' else colors[color_index]
                        objects.append({
                            'type': tool, 
                            'start': current_shape_start, 
                            'end': event.pos, 
                            'color': active_color, 
                            'radius': radius
                        })
                    drawing = False
                    current_shape_start = None

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'brush' or tool == 'eraser':
                    objects[-1]['points'].append(event.pos)

        # Rendering all objects 
        for obj in objects:
            draw_object(screen, obj)
        
        # Предпросмотр (пока тянем мышь)
        if drawing and current_shape_start:
            mouse_pos = pygame.mouse.get_pos()
            active_color = (0, 0, 0) if tool == 'eraser' else colors[color_index]
            if tool not in ['brush', 'eraser']:
                temp_obj = {'type': tool, 'start': current_shape_start, 'end': mouse_pos, 'color': active_color, 'radius': radius}
                draw_object(screen, temp_obj)

        # Вывод информации о текущих настройках
        display_info(screen, tool, colors[color_index], radius)

        pygame.display.flip()
        clock.tick(60)

def draw_object(screen, obj):
    if obj['type'] == 'line':
        for i in range(len(obj['points']) - 1):
            pygame.draw.line(screen, obj['color'], obj['points'][i], obj['points'][i+1], obj['radius'] * 2)
            pygame.draw.circle(screen, obj['color'], obj['points'][i], obj['radius'])
            
    elif obj['type'] == 'rectangle':
        x1, y1 = obj['start']
        x2, y2 = obj['end']
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
        # if width 0 paints over a figure, width > 0 draws frame
        pygame.draw.rect(screen, obj['color'], rect, max(1, obj['radius']))
        
    elif obj['type'] == 'circle':
        x1, y1 = obj['start']
        x2, y2 = obj['end']
        dist = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
        if dist > 0:
            pygame.draw.circle(screen, obj['color'], (x1, y1), dist, max(1, obj['radius']))

def display_info(screen, tool, color, radius):
    font = pygame.font.SysFont("Arial", 18)
    text = f"Tool: {tool.upper()} (1-4) | Color: {color} (5 to change) | Radius: {radius}"
    img = font.render(text, True, (255, 255, 255))
    # Painting little preview of color
    pygame.draw.rect(screen, color, (10, 35, 30, 15))
    screen.blit(img, (10, 10))

main()