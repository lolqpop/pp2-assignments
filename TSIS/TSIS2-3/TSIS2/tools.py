import pygame

def flood_fill(surface, x, y, new_color):
    """Fills a closed area with a new color using BFS."""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    width, height = surface.get_size()
    queue = [(x, y)]
    
    # Use a set to keep track of visited pixels for performance
    visited = set([(x, y)])

    while queue:
        curr_x, curr_y = queue.pop(0)
        
        # Set the color of the current pixel
        surface.set_at((curr_x, curr_y), new_color)

        # Check neighbors (Up, Down, Left, Right)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            
            if 0 <= nx < width and 0 <= ny < height:
                if surface.get_at((nx, ny)) == target_color and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))