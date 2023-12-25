#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import math

def draw_circle(draw, center_x, center_y, size, aspect_ratio, color):
    radius = size / 2
    draw.ellipse([(center_x - radius, center_y - radius),
                  (center_x + radius, center_y + radius)], fill=color)

def draw_oval(draw, center_x, center_y, size, aspect_ratio, color):
    aspect_ratio = aspect_ratio
    draw.ellipse([(center_x - size / 2, center_y - size / 2 / aspect_ratio),
                  (center_x + size / 2, center_y + size / 2 / aspect_ratio)], fill=color)

def draw_diamond(draw, center_x, center_y, size, aspect_ratio, color):
    aspect_ratio = aspect_ratio
    draw.polygon([(center_x, center_y - size / 2 / aspect_ratio),
                  (center_x + size / 2, center_y),
                  (center_x, center_y + size / 2 / aspect_ratio),
                  (center_x - size / 2, center_y)], fill=color)

def draw_square(draw, center_x, center_y, size, aspect_ratio, color):
    draw.rectangle([(center_x - size / 2, center_y - size / 2),
                    (center_x + size / 2, center_y + size / 2)], fill=color)

def draw_triangle(draw, center_x, center_y, size, aspect_ratio, color):
    draw.polygon([(center_x, center_y - size / 2),
                  (center_x + size / 2, center_y + size / 2),
                  (center_x - size / 2, center_y + size / 2)], fill=color)

def draw_hexagon(draw, center_x, center_y, size, aspect_ratio, color):
    hexagon_points = [
        (center_x - size / 2, center_y),
        (center_x - size / 4, center_y - size / 2),
        (center_x + size / 4, center_y - size / 2),
        (center_x + size / 2, center_y),
        (center_x + size / 4, center_y + size / 2),
        (center_x - size / 4, center_y + size / 2)
    ]
    draw.polygon(hexagon_points, fill=color)

def draw_octagon(draw, center_x, center_y, size, aspect_ratio, color):
    octagon_points = [
        (center_x - size / 2, center_y - size / 4),
        (center_x - size / 4, center_y - size / 2),
        (center_x + size / 4, center_y - size / 2),
        (center_x + size / 2, center_y - size / 4),
        (center_x + size / 2, center_y + size / 4),
        (center_x + size / 4, center_y + size / 2),
        (center_x - size / 4, center_y + size / 2),
        (center_x - size / 2, center_y + size / 4),
    ]
    draw.polygon(octagon_points, fill=color)

def draw_quarter_circle(draw, center_x, center_y, size, aspect_ratio, color):
    draw.pieslice([(center_x - size / 2, center_y - size / 2),
                   (center_x + size / 2, center_y + size / 2)], start=0, end=90, fill=color)

def draw_half_circle(draw, center_x, center_y, size, aspect_ratio, color):
    draw.pieslice([(center_x - size / 2, center_y - size / 2),
                   (center_x + size / 2, center_y + size / 2)], start=0, end=180, fill=color)

def draw_starburst(draw, center_x, center_y, size, aspect_ratio, color):
    num_rays = 16
    for i in range(num_rays):
        angle_ray = math.radians(i * (360 / num_rays))
        x_end = center_x + size / 2 * math.cos(angle_ray)
        y_end = center_y + size / 2 * math.sin(angle_ray)
        draw.line([(center_x, center_y), (x_end, y_end)], fill=color, width=int(size / 20))

def draw_star(draw, center_x, center_y, size, aspect_ratio, color):
    outer_radius = size / 4
    inner_radius = outer_radius * math.cos(math.radians(36)) / math.cos(math.radians(72))
    angle = -math.pi / 2

    star_points = []
    for _ in range(5):
        x_outer = center_x + outer_radius * math.cos(angle)
        y_outer = center_y + outer_radius * math.sin(angle)
        star_points.extend([x_outer, y_outer])
        angle += math.radians(72)

        x_inner = center_x + inner_radius * math.cos(angle)
        y_inner = center_y + inner_radius * math.sin(angle)
        star_points.extend([x_inner, y_inner])
        angle += math.radians(72)

    draw.polygon(star_points, fill=color)
 
def draw_cross(draw, center_x, center_y, size, aspect_ratio, color):
    # Define the points for the cross arms
    cross_points = [
        (center_x - size / 6, center_y - size / 2),
        (center_x + size / 6, center_y - size / 2),
        (center_x + size / 6, center_y - size / 6),
        (center_x + size / 2, center_y - size / 6),
        (center_x + size / 2, center_y + size / 6),
        (center_x + size / 6, center_y + size / 6),
        (center_x + size / 6, center_y + size / 2),
        (center_x - size / 6, center_y + size / 2),
        (center_x - size / 6, center_y + size / 6),
        (center_x - size / 2, center_y + size / 6),
        (center_x - size / 2, center_y - size / 6),
        (center_x - size / 6, center_y - size / 6), 
    ]
    draw.polygon(cross_points, fill=color)

