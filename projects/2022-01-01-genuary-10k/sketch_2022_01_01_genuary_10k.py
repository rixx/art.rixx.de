from functools import partial
import math
import vsketch

BIG = 4.4
POS_WOBBLE = 0.5
SIZE_WOBBLE = 0.5

class Genuary10kSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw_line_segment(self, start, end, radius, distance):
        start = (start[0]*BIG, start[1]*BIG)
        end = (end[0]*BIG, end[1]*BIG)
        num_steps = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1])**2) / distance

        x_gradient = (end[0] - start[0]) / num_steps
        y_gradient = (end[1] - start[1]) / num_steps

        x_pos = start[0]
        y_pos = start[1]

        for _ in range(int(num_steps)):
            self.vsk.circle(
                x_pos + self._vsk.random(-POS_WOBBLE*radius, POS_WOBBLE*radius),
                y_pos + self._vsk.random(-POS_WOBBLE*radius, POS_WOBBLE*radius),
                radius + self._vsk.random(-SIZE_WOBBLE*radius, SIZE_WOBBLE*radius),
                mode="radius",
            )
            x_pos += x_gradient
            y_pos += y_gradient
        return int(num_steps)

    def draw_line(self, points, radius, distance):
        num_steps = 0
        for index in range(len(points) - 1):
            num_steps += self.draw_line_segment(points[index], points[index + 1], radius, distance)
        return num_steps


    def draw_two(self, x, y, radius, distance):
        return self.draw_line([
            (x, y),
            (x+ 1, y),
            (x+ 1, y+1),
            (x, y+1),
            (x, y+2),
            (x+ 1.1, y+2),
        ], radius, distance)


    def draw(self, vsk: vsketch.Vsketch) -> None:
        self._vsk = vsk
        vsk.size("a3", landscape=True)
        vsk.scale("cm")
        vsk.penWidth("0.1mm", 1)
        vsk.stroke(1)

        radius = 0.7
        distance = 0.04

        total_steps = self.draw_two(0, 0, radius=radius, distance=distance)
        total_steps += self.draw_two(4, 0, radius=radius, distance=distance)
        total_steps += self.draw_two(6, 0, radius=radius, distance=distance)
        total_steps += self.draw_line([
            (2, 0),
            (3,0),
            (3,2),
            (2,2),
            (2,0),
            ], radius, distance)
        total_steps += self.draw_line([
            (-1, -2),
            (-1, 4),
            (8, 4),
            (8, -2),
            (-1, -2),
            ], 0.7, 0.08)
        total_steps += self.draw_line([
            (-1, -2),
            (-1, 4),
            (8, 4),
            (8, -2),
            (-1, -2),
            ], 0.1, 0.02)

        print(total_steps)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Genuary10kSketch.display()
