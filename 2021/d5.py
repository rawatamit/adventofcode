from point import Point2D
import re


class Line:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end
    
    def start_x(self):
        return self.start.x

    def start_y(self):
        return self.start.y

    def end_x(self):
        return self.end.x

    def end_y(self):
        return self.end.y
    
    def is_horizontal(self):
        return self.start.x == self.end.x or self.start.y == self.end.y
    
    def is_inside(self, x, y):
        P = Point2D(x, y)
        AP = self.start.euclidean_distance(P)
        PB = P.euclidean_distance(self.end)
        AB = self.start.euclidean_distance(self.end)
        return AB == AP + PB


def grid_bounds(segments):
    min_x = min(segment.start_x() for segment in segments)
    max_x = max(segment.end_x() for segment in segments)
    min_y = min(segment.start_y() for segment in segments)
    max_y = max(segment.end_y() for segment in segments)
    return min_x, max_x, min_y, max_y


def make_grid(max_x, max_y):
    return [[0 for _ in range(max_x + 1)]
            for _ in range(max_y + 1)]


def fill_with_segment(segment, grid):
    sx = segment.start_x()
    sy = segment.start_y()
    ex = segment.end_x()
    ey = segment.end_y()

    if sx == ex:
        x = sx
        ry = range(sy, ey+1) if sy < ey else range(sy, ey-1, -1)
        for y in ry:
            grid[y][x] += 1
    else:
        y = sy
        rx = range(sx, ex+1) if sx < ex else range(sx, ex-1, -1)
        for x in rx:
            grid[y][x] += 1


def fill_with_segment_diagonal(segment, grid):
    sx = segment.start_x()
    sy = segment.start_y()
    ex = segment.end_x()
    ey = segment.end_y()

    rx = range(sx, ex+1) if sx < ex else range(sx, ex-1, -1)
    ry = range(sy, ey+1) if sy < ey else range(sy, ey-1, -1)

    for x, y in zip(rx, ry):
        grid[y][x] += 1


def populate_grid(segments):
    min_x, max_x, min_y, max_y = grid_bounds(segments)
    max_axis = max(max_x, max_y)
    grid = make_grid(max_axis, max_axis)

    for segment in segments:
        if segment.is_horizontal():
            fill_with_segment(segment, grid)
        else:
            fill_with_segment_diagonal(segment, grid)
    
    count = 0
    for row in grid:
        for x in row:
            if x >= 2: count += 1
    
    print(count)


if __name__ == '__main__':
    regex = r'(\d+),(\d+)\s+->\s+(\d+),(\d+)'
    segments = []

    with open('d5.txt') as fin:
        for line in fin:
            if groups := re.search(regex, line):
                sx = int(groups.group(1))
                sy = int(groups.group(2))
                ex = int(groups.group(3))
                ey = int(groups.group(4))
                segments.append(Line(Point2D(sx, sy), Point2D(ex, ey)))
    
    populate_grid(segments)
