import vsketch
import math

class Vsk:
    def __init__(self, vsk=None):
        self.v = vsk
        super().__init__()

    def rand_int(self, minimum, maximum):
        return int(self.v.random(minimum, maximum + 1))

def rotate_point(x, y, degrees, origin=None):
    rotate_x, rotate_y = origin if origin else (0, 0)
    if rotate_x != 0:
        x -= rotate_x
    if rotate_y != 0:
        y -= rotate_y

    radians = degrees * (math.pi / 180)
    rotate_sin = round(math.sin(radians), 3)
    rotate_cos = round(math.cos(radians), 3)

    new_x = x * rotate_cos - y * rotate_sin
    new_y = y * rotate_cos + x * rotate_sin

    return new_x + rotate_x, new_y + rotate_y


def distance(left_x, left_y, right_x, right_y):
    return math.sqrt(
        (left_x - right_x)**2 + (left_y - right_y)**2
    )


def midpoint(left_x, left_y, right_x, right_y):
    return (
        right_x + (left_x-right_x) /2,
        right_y + (left_y - right_y)/2
    )

class RoseWindow(Vsk):

    def __init__(self, *args, width=None, center=None):
        super().__init__(*args)
        self.width = width or 200
        self.center = center or (0, 0)

    def draw(self):
        outer_radius = self.width
        inner_radius = self.rand_int(20, 0.2 * self.width)
        segments = self.rand_int(3, 5) * 4
        segment_degrees = 360/segments
        segment_gap = 0.5
        segment_width = segment_degrees - segment_gap
        arc_height = outer_radius * 1.32
        circle_radius = 36

        self.v.translate(-self.center[0], -self.center[1])
        window_sketch = vsketch.Vsketch()

        self.draw_circle(window_sketch, 0, 0, inner_radius, decoration_symmetry=5)
        window_sketch.circle(0, 0, arc_height + 1, mode="radius")
        window_sketch.circle(0, 0, arc_height + 3, mode="radius")

        inner_rotation = segment_degrees - 2 * segment_gap
        outer_left = (0, outer_radius)
        inner_left = (0, inner_radius)
        left_arc_center = rotate_point(-2.5, outer_radius + (arc_height - outer_radius)*0.42, segment_width*0.25)
        right_arc_center = rotate_point(2.5, outer_radius + (arc_height - outer_radius)*0.42, segment_width*0.75)
        outer_right = rotate_point(0, outer_radius, inner_rotation)
        inner_right = rotate_point(0, inner_radius, inner_rotation)
        outer_center = midpoint(*outer_right, *outer_left)
        inner_center = midpoint(*inner_right, *inner_left)
        center = rotate_point(0, arc_height, segment_width/2)
        circle_center = rotate_point(0, arc_height-24, segment_width/2)
        # segments = 1
        for window_degree in range(segments):
            segment_sketch = vsketch.Vsketch()
            
            segment_sketch.line(*inner_left, *outer_left)
            segment_sketch.line(*inner_right, *outer_right)
            segment_sketch.line(*inner_center, *outer_center)

            self.draw_arc(segment_sketch, outer_left, center, outer_right, segment_width)
            self.draw_arc(segment_sketch, outer_left, left_arc_center, outer_center, segment_width / 2)
            self.draw_arc(segment_sketch, outer_center, right_arc_center, outer_right, segment_width / 2, initial_rotation=segment_width*0.5)
            # TODO make circle radius and circle_center fitting
            self.draw_circle(segment_sketch, *circle_center, 17)

            window_sketch.rotate(segment_degrees * window_degree, degrees=True)
            window_sketch.sketch(segment_sketch)
            window_sketch.rotate(-segment_degrees * window_degree, degrees=True)

        self.v.sketch(window_sketch)
        self.v.translate(*self.center)

    def draw_arc(self, sketch, left, center, right, degrees, initial_rotation=0):

        unrotated_left = rotate_point(*left, -initial_rotation)
        unrotated_center = rotate_point(*center, -initial_rotation/2)

        arc_height = abs(unrotated_center[1] - unrotated_left[1])
        anchor_height = unrotated_left[1] + arc_height * 0.75
        arc_width = distance(*left, *right)

        lower_anchor = arc_width * 0.2
        upper_anchor = arc_width * 0.1

        left_anchor = rotate_point(-lower_anchor, anchor_height, initial_rotation)
        right_anchor = rotate_point(lower_anchor, anchor_height, degrees + initial_rotation)
        center_left_anchor = rotate_point(upper_anchor, arc_height, degrees / 2 + initial_rotation)
        center_right_anchor = rotate_point(-upper_anchor, arc_height, degrees / 2 + initial_rotation)

        sketch.bezier(*left, *left_anchor, *center, *center)
        sketch.bezier(*center, *center, *right_anchor, *right)
        # sketch.bezier(*left, *left_anchor, *center_left_anchor, *center)
        # sketch.bezier(*center, *center_right_anchor, *right_anchor, *right)

    def draw_circle(self, sketch, x, y, radius, decoration_symmetry=5):
        sketch.translate(x, y)
        sketch.circle(0, 0, radius, mode="radius")
        segment_rotation = int(360/decoration_symmetry)
        inner_radius = radius * (1 - decoration_symmetry * 0.05)
        inner_x = radius * (0.35 + decoration_symmetry * 0.05)
        for _ in range(decoration_symmetry):
            sketch.arc(inner_x, 0, inner_radius, inner_radius, 220, 140, degrees=True)
            sketch.rotate(segment_rotation, degrees=True)
        sketch.translate(-x, -y)

class Cathedral(Vsk):
    def draw(self):
        center_width = self.rand_int(150, 250)
        rose_window = RoseWindow(self.v, width=center_width - 20, center=(10,10))
        rose_window.draw()


class WindowsSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw_line(self, start_x, start_y, end_x, end_y, rotate_degrees=None, rotate_origin=None):
        if rotate_degrees:
            start_x, start_y = self.rotate_point(start_x, start_y, rotate_degrees, rotate_origin)
            end_x, end_y = self.rotate_point(end_x, end_y, rotate_degrees, rotate_origin)
        self.v.line(start_x, start_y, end_x, end_y)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        cathedral = Cathedral(vsk)
        cathedral.draw()

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        return
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    WindowsSketch.display()
