import pygame
from collections import deque

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    width, height = surface.get_size()
    queue = deque([(x, y)])
    visited = set([(x, y)])

    while queue:
        cx, cy = queue.popleft()
        surface.set_at((cx, cy), new_color)

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited and surface.get_at((nx, ny)) == target_color:
                    visited.add((nx, ny))
                    queue.append((nx, ny))