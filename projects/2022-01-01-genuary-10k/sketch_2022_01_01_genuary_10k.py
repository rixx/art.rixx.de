from functools import partial
import math
import vsketch

BIG = 3.8
POS_WOBBLE = 0.5
SIZE_WOBBLE = 0.5


class Point:
    def __init__(self, x, y, left_arc=None, right_arc=None):
        self.x = x
        self.y = y
        self.left_arc = left_arc
        self.right_arc = right_arc

    def zoom(self, factor):
        left_arc = None
        right_arc = None

        if self.left_arc:
            left_arc =self.left_arc.zoom(factor)
        if self.right_arc:
            right_arc = self.right_arc.zoom(factor)
        return Point(self.x * factor, self.y*factor, left_arc=left_arc, right_arc=right_arc)

    def __str__(self):
        return f"x={self.x}, y={self.y}"

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return True


class Genuary10kSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def _draw_at(self, x, y, radius):
        self.vsk.circle(
            x + self._vsk.random(-POS_WOBBLE*radius, POS_WOBBLE*radius),
            y + self._vsk.random(-POS_WOBBLE*radius, POS_WOBBLE*radius),
            radius + self._vsk.random(-SIZE_WOBBLE*radius, SIZE_WOBBLE*radius),
            mode="radius",
        )

    def get_point_distance(self, *points):
        total = 0
        for index in range(len(points) - 1):
            start = points[index]
            end = points[index + 1]
            total += math.sqrt((start.x - end.x) ** 2 + (start.y - end.y)**2)
        return total

    def draw_line_segment(self, start, end, radius, distance):
        start = start.zoom(BIG)
        end = end.zoom(BIG)
        num_steps = self.get_point_distance(start, end) / distance

        x_gradient = (end.x - start.x) / num_steps
        y_gradient = (end.y - start.y) / num_steps

        x_pos = start.x
        y_pos = start.y

        for _ in range(int(num_steps)):
            self._draw_at(x_pos, y_pos, radius)
            x_pos += x_gradient
            y_pos += y_gradient
        return int(num_steps)

    def _line_percent(self, start, end, percent):
        if start.x == end.x and start.y == end.y:
            return start
        return Point(
            start.x + (end.x - start.x)*percent,
            start.y + (end.y - start.y)*percent,
        )


    def draw_curve_segment(self, start, end, radius, distance):
        start = start.zoom(BIG)
        end = end.zoom(BIG)

        x_pos = start.x
        y_pos = start.y
        curve_points = [start, start.right_arc or start, end.left_arc or end, end]
        num_steps = 0.7*self.get_point_distance(*curve_points) / distance

        for step in range(int(num_steps)):
            position = step/num_steps
            point_left = self._line_percent(curve_points[0], curve_points[1], position)
            point_center = self._line_percent(curve_points[1], curve_points[2], position)
            point_right = self._line_percent(curve_points[2], curve_points[3], position)
            point_lefter = self._line_percent(point_left, point_center, position)
            point_righter = self._line_percent(point_center, point_right, position)
            real_point = self._line_percent(point_lefter, point_righter, position)
            self._draw_at(real_point.x, real_point.y, radius)
        return int(num_steps)
            

    def draw_line(self, points, radius, distance):
        num_steps = 0
        for index in range(len(points) - 1):
            start = points[index]
            end = points[index + 1]
            if not start.right_arc and not end.left_arc:
                num_steps += self.draw_line_segment(start, end, radius, distance)
            else:
                num_steps += self.draw_curve_segment(start, end, radius, distance)
        return num_steps


    def draw_two_lines(self, x, y, radius, distance):
        return self.draw_line([
            Point(x, y),
            Point(x+ 1, y),
            Point(x+ 1, y+1),
            Point(x, y+1),
            Point(x, y+2),
            Point(x+ 1.1, y+2),
        ], radius, distance)

    def draw_two_curves(self, x, y, radius, distance):
        return self.draw_line([
            Point(x, y+0.2, right_arc=Point(x + 0.2, y-0.2)),
            Point(x+1, y, left_arc=Point(x + 0.8, y - 0.2), right_arc=Point(x+1.6, y+0.8)),
            Point(x, y+2, left_arc=Point(x+0.1, y+2.4), right_arc=Point(x+0.3, y+1.7)),
            Point(x+1.35, y+2, left_arc=Point(x+0.8, y+2.5)),
        ], radius, distance)


    def draw(self, vsk: vsketch.Vsketch) -> None:
        self._vsk = vsk
        vsk.size("a3", landscape=True)
        vsk.scale("cm")
        vsk.penWidth("0.1mm", 1)
        vsk.stroke(1)

        # radius = 0.7
        # distance = 0.04
        radius = 0.5
        distance = 0.04
        total_steps = 0

        total_steps += self.draw_two_curves(0, 3, radius=radius, distance=distance)
        total_steps += self.draw_two_curves(4, 3, radius=radius, distance=distance)
        total_steps += self.draw_two_curves(6, 3, radius=radius, distance=distance)
        total_steps += self.draw_line([
            Point(1.9, 4, right_arc=Point(2, 2.4)),
            Point(3.3, 4, left_arc=Point(3.2, 2.4), right_arc=Point(3.3, 5.6)),
            Point(1.9, 4, left_arc=Point(1.8, 5.6)),
            ], radius, distance)

        # print numbers without curves
        total_steps += self.draw_two_lines(0, 0, radius=radius, distance=distance)
        total_steps += self.draw_two_lines(4, 0, radius=radius, distance=distance)
        total_steps += self.draw_two_lines(6, 0, radius=radius, distance=distance)
        total_steps += self.draw_line([
            Point(2, 0),
            Point(3,0),
            Point(3,2),
            Point(2,2),
            Point(2,0),
            ], radius, distance)

        # print border
        total_steps += self.draw_line([
            Point(-1, -1),
            Point(-1, 6),
            Point(8, 6),
            Point(8, -1),
            Point(-1, -1),
            ], 0.7, 0.08)
        total_steps += self.draw_line([
            Point(-1, -1),
            Point(-1, 6),
            Point(8, 6),
            Point(8, -1),
            Point(-1, -1),
            ], 0.15, 0.0272)

        print(total_steps)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Genuary10kSketch.display()
