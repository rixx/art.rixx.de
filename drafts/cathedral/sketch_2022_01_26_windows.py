import vsketch
import math


class WindowsSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def rotate_point(self, x, y, degrees, origin=None):
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

    def draw_line(self, start_x, start_y, end_x, end_y, rotate_degrees=None, rotate_origin=None):
        if rotate_degrees:
            start_x, start_y = self.rotate_point(start_x, start_y, rotate_degrees, rotate_origin)
            end_x, end_y = self.rotate_point(end_x, end_y, rotate_degrees, rotate_origin)
        self.v.line(start_x, start_y, end_x, end_y)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        self.v = vsk
        # vsk.scale("cm")

        inner_radius = 20
        outer_radius = 200
        # segments = 16
        segments = int(self.v.random(3, 5)) * 4
        segments = 16
        segment_degrees = 360/segments
        segment_gap = 1
        segment_width = (segment_degrees - segment_gap) / 2
        arc_height = outer_radius * 1.35
        circle_radius = 36

        # implement your sketch here
        vsk.circle(0, 0, inner_radius, mode="radius")
        # vsk.circle(0, 0, outer_radius, mode="radius")

        for window_degree in range(segments):
            base_offset = segment_degrees * window_degree

            left_point = self.rotate_point(0, outer_radius, base_offset + segment_gap, (0, 0))
            center_point = self.rotate_point(0, arc_height, base_offset + segment_gap + segment_width)
            circle_center_point = self.rotate_point(0, arc_height - circle_radius*0.7, base_offset + segment_gap + segment_width)
            right_point = self.rotate_point(0, outer_radius, base_offset + segment_gap + 2 * segment_width)

            anchor_height = outer_radius * 1.22
            left_anchor = self.rotate_point(0, anchor_height, base_offset + segment_gap, (0, 0))
            right_anchor = self.rotate_point(0, anchor_height, base_offset + segment_gap + 2 * segment_width)
            center_left_anchor = self.rotate_point(5, arc_height, base_offset + segment_gap + segment_width, (0, 0))
            center_right_anchor = self.rotate_point(-5, arc_height, base_offset + segment_gap + segment_width)

            self.draw_line(0, inner_radius, 0, outer_radius, base_offset + segment_gap)
            self.draw_line(0, inner_radius, 0, outer_radius, base_offset+segment_gap + segment_width)
            self.draw_line(0, inner_radius, 0,outer_radius,base_offset+segment_gap+2*segment_width)

            vsk.bezier(*left_point, *left_anchor, *center_left_anchor, *center_point)
            vsk.bezier(*center_point, *center_right_anchor, *right_anchor, *right_point)

            vsk.circle(*circle_center_point, circle_radius)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    WindowsSketch.display()
