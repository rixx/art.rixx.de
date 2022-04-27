import datetime as dt
import vsketch

SQUARE_SIZE = 0.4
SQUARE_GAP = 0.1
DAY_GAP = 0.4
MARGIN_TOP = 1
MARGIN_LEFT = 1

DAY_SIZE = SQUARE_SIZE * 4 + SQUARE_GAP * 3


class PlannerSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw_day_group(self, left, top, day=None):
        empty = ((1, 1), (1, 2), (2, 1), (2, 2))
        for row in range(4):
            for column in range(4):
                if (row, column) in empty:
                    continue
                _top = top + row * (SQUARE_SIZE + SQUARE_GAP)
                _left = left + column * (SQUARE_SIZE + SQUARE_GAP)
                self.v.square(_left, _top, SQUARE_SIZE)
        if day:
            self.v.text(
                x=left + SQUARE_SIZE + SQUARE_GAP,
                y=top + DAY_SIZE / 2,
                width=2 * SQUARE_SIZE + SQUARE_GAP,
                text=str(day.day),
                align="center",
                size="0.5pt",
                font="cursive",
            )

    def draw(self, vsk: vsketch.Vsketch) -> None:
        self.v = vsk
        vsk.size("a3", landscape=False)
        vsk.scale("cm")
        counter = 0
        rows = 16
        columns = 11
        total_days = rows * columns
        day = dt.date(day=21, month=10, year=2022) - dt.timedelta(days=total_days - 1)
        for row in range(rows):
            for column in range(columns):
                top = MARGIN_TOP + row * (DAY_SIZE + DAY_GAP)
                left = MARGIN_LEFT + column * (DAY_SIZE + DAY_GAP)
                self.draw_day_group(left, top, day=day)
                day += dt.timedelta(days=1)
                counter += 1
        print(f"{counter}/178, {178-counter}")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PlannerSketch.display()
