import math
import random
import sys
import matplotlib.pyplot as pl
import matplotlib.patches as patches
import matplotlib as mpl

def random_rectangle(center_x, center_y, radius, eps=0.1):
    """Create random rectangle (x, y, l, w, r) inside a given circle."""
    min_length = eps * radius
    max_length = (1 - eps) * radius
    length = random.uniform(min_length, max_length) # half length, since radius is half diameter
    width = math.sqrt(radius ** 2 - length ** 2) # half width, since radius is half diameter
    rotation = random.uniform(0, 90) # in degrees
    scalar = 0.999 # make it a bit smaller, as we discussed
    return (center_x, center_y, scalar * length * 2, scalar * width * 2, rotation)

def get_subrectangles(x, y, l, w, r, count=4):
    """Subdivide the rectangle in x and y direction count times"""
    r_radian = math.pi * r / 180
    x1 = x - l / 2
    x2 = x + l / 2
    xmin = min([x1, x2])
    xmax = max([x1, x2])
    xdiff = xmax - xmin

    y1 = y - w / 2
    y2 = y + w / 2
    ymin = min([y1, y2])
    ymax = max([y1, y2])
    ydiff = ymax - ymin

    rectangles = []
    for i in range(count):
        for j in range(count):
            rxmin = xmin + i * xdiff / count
            rx = rxmin + xdiff / (2 * count)
            rymin = ymin + j * ydiff / count
            ry = rymin + (ydiff / (2 * count))
            rl = l / count
            rw = w / count

            dx = rx - x
            dy = ry - y

            # Rotation matrix c, -s; s, c
            newdx = math.cos(r_radian) * dx - math.sin(r_radian) * dy
            newdy = math.sin(r_radian) * dx + math.cos(r_radian) * dy

            rectangles.append((x + newdx, y + newdy, rl, rw, r))

    return rectangles


def single_circle_coverage(x, y, l, w, r):
    """Create a circle (center_x, center_y, radius) that encompases a given
    rectangle (x, y, l, w, r)"""
    return (x, y, math.sqrt((l/2) ** 2 + (w/2) ** 2))


def circle_coverage(x, y, l, w, r, subdivision_count=4):
    """Create subdivision_count^2 number of circles (center_x, center_y, radius)
    that together encompass a given rectangle (x, y, l, w, r) with r in
    degrees indicating counterclockwise rotation"""

    circles = []
    for subrectangle in get_subrectangles(x, y, l, w, r, subdivision_count):
        circles.append(single_circle_coverage(*subrectangle))

    return circles

def random_nonintersecting_circle(center_x, center_y, upper_b, lower_b, left_b, right_b, other_circles):
    """Given other_circles (as a list of (cx, cy, radius)), find the largest circle
    that does not intersect with other circles"""
    radius = sys.float_info.max
    for (other_x, other_y, other_radius) in other_circles:
        distance = math.sqrt((other_x - center_x)**2 + (other_y - center_y)**2)
        boundary_distance = get_boundary_distance(center_x, center_y, upper_b, lower_b, left_b, right_b)
        radius = min([radius, distance - other_radius, boundary_distance])
    if radius <= 0:
        return None
    else:
        coeff = random.uniform(0.5, 0.9)
        return center_x, center_y, coeff * radius

def random_nonintersecting_rectangle(center_x, center_y, upper_b, lower_b, left_b, right_b, other_rectangles, subdivision_count=4):
    """Given other_rectangles (as a list of (x, y, l, w, r)), return a random rectangle
    inside the largest circle that does not intersect with the circles that cover the other rectangles."""
    all_other_circles = []
    print(other_rectangles)
    for other_rectangle in other_rectangles:
        all_other_circles += circle_coverage(*other_rectangle, subdivision_count)
    circle = random_nonintersecting_circle(center_x, center_y, upper_b, lower_b, left_b, right_b, all_other_circles)
    if circle is not None:
        return random_rectangle(*circle)
    else:
        return None

def get_boundary_distance(center_x, center_y, upper_b, lower_b, left_b, right_b):
    upper_distance = upper_b - center_y
    lower_distance = center_y - lower_b
    left_distance = center_x - left_b
    right_distance = right_b - center_x
    return min([upper_distance, lower_distance, left_distance, right_distance])

def plot_rectangle(rectangles):
    for (x, y, l, w, r) in rectangles:
        pl.plot([x], [y], color="#FF000030", marker='o', markersize=10)
        rect = patches.Rectangle((x - l / 2, y - w / 2), l, w, color="#FF000030", alpha=0.10, angle=r, rotation_point='center')
        ax = pl.gca()
        ax.add_patch(rect)
    pl.figure()
    pl.plot()
    pl.xlim([-10, 150])
    pl.ylim([-10, 150])
    pl.show()



if __name__ == "__main__":


    def plot_rectangle_and_coverage_circles(rectangle, color, draw_coverage=True, subdivision_count=4):
        (x, y, l, w, r) = rectangle
        pl.plot([x], [y], color=color, marker='o', markersize=10)
        rect = patches.Rectangle((x-l/2,y-w/2), l, w, color=color, alpha=0.10, angle=r, rotation_point='center')
        ax = pl.gca()

        ax.add_patch(rect)

        if draw_coverage:
            circles = circle_coverage(x, y, l, w, r, subdivision_count)
            for (cx, cy, radius) in circles:
                pl.plot([cx], [cy], marker="x", markersize=5, color="red")
                circle = patches.Circle((cx, cy), radius, color="#FF000030", alpha=0.1)
                ax.add_patch(circle)

    pl.figure()
    pl.plot()
    pl.xlim([-10, 150])
    pl.ylim([-10, 150])

    subdivision_count = 4
    # x, y, l, w, r
    rectangle1 = (10, 30, 40, 40, 10)
    plot_rectangle_and_coverage_circles(rectangle1, "blue", subdivision_count=subdivision_count)

    rectangle2 = (90, 30, 50, 50, 90)
    plot_rectangle_and_coverage_circles(rectangle2, "blue", subdivision_count=subdivision_count)

    new_rectangle = random_nonintersecting_rectangle(35, 15, 100, -100, -100, 100, [rectangle1, rectangle2], subdivision_count=subdivision_count)
    plot_rectangle_and_coverage_circles(new_rectangle, "green", True, 1)

    pl.show()