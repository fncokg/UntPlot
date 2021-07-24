import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle, FancyArrowPatch
import numpy as np
from itertools import cycle

plt.rcParams["font.sans-serif"] = ["SimHei"]
SQRT2 = np.sqrt(2)


class UntPlotBase:
    # zorder:
    #   1 : grid
    #   2 : lines
    #   3 : arrow on lines
    #   4 : point marker
    #   5 : text on markers
    def __init__(self, figsize=(14, 14), grid_color="grey"):
        self.fig, self.ax = plt.subplots(figsize=(14, 14))
        plt.axis("off")
        self.grid_color = grid_color
        self._draw_grid()

    def _draw_grid(self):
        # Draw a 5x5 grid, whose color is defined in self.grid_color
        for i in range(1, 6):
            for p1, p2 in [[(1, i), (5, i)], [(i, 1), (i, 5)]]:
                p1, p2 = self._coord_trans(*p1), self._coord_trans(*p2)
                self.ax.plot(*zip(p1, p2), color=self.grid_color, zorder=1)

    def _coord_trans(self, x, y):
        # Transformation from target coordinates(five levels) to real coordinates
        return (y - x) / SQRT2, (y + x) / SQRT2

    def create_point(self, x, y, name, color, trans=True):
        """
        Create an Unt-style point.

        Parameters
        ----------
        x, y : int
            coordinates
        name : str
            text on the marker
        color : str
            any valid matplotlib color description
        trans : bool, optional
            whether to transform the x,y coordinates towards real coordinates, by default True
        """
        if trans:
            x, y = self._coord_trans(x, y)
        self.ax.scatter(x, y, color=color, s=4000, zorder=4)
        self.ax.annotate(
            name,
            xy=(x, y),
            zorder=5,
            va="center",
            ha="center",
            color="white",
            fontsize=32,
        )

    def create_arrow_line(self, p1, p2, color, linewidth=4, trans=True):
        """
        Create an Unt-style arrowed line.

        Parameters
        ----------
        p1, p2 : 2d-array like
            draw line from p1 to p2
        color : str
            any valid matplotlib color description
        linewidth : int, optional
            linewdith of the line and the arrow, by default 4
        trans : bool, optional
            whether to transform the x,y coordinates towards real coordinates, by default True
        """
        if trans:
            p1, p2 = self._coord_trans(*p1), self._coord_trans(*p2)
        middle_point = [i + 0.6 * (j - i) for i, j in zip(p1, p2)]
        d_middle_point = [i + 0.49 * (j - i) for i, j in zip(p1, p2)]
        arrow_style = ArrowStyle("->", head_length=20, head_width=12)
        arrow = FancyArrowPatch(
            d_middle_point,
            middle_point,
            arrowstyle=arrow_style,
            color=color,
            lw=linewidth,
            zorder=3,
        )
        self.ax.add_patch(arrow)
        self.ax.plot(*zip(p1, p2), color=color, lw=linewidth, zorder=2)


class UntPlot(UntPlotBase):
    def __init__(self, *args, **kwargs):
        self.color_map = [
            "#FDCD00",
            "#A46F24",
            "#91D285",
            "#70916F",
            "#0190E4",
            "#3750A5",
            "#B4C3D9",
            "#69666F",
        ]
        self.color_names = list("金茶草柳蔚靛雪墨")
        self.tonal_names = [f"{prefix}{suffix}" for suffix in "平上去入" for prefix in "阴阳"]
        self.color_iter = cycle(self.color_map)
        super(UntPlot, self).__init__(*args, **kwargs)

    def tonal_value2coord(self, value):
        """
        Transform tonal value to real coordinates.

        Parameters
        ----------
        value : str
            Five-level tonal vales such as "51"

        Returns
        -------
        tuple
            2d int tuple, real coordinates of the tonal value
        """
        assert len(value) in [2, 3]
        coord = tuple(map(int, value))
        if len(coord) == 2:
            return self._coord_trans(*coord)
        else:
            start, middle, end = coord
            height = 0.25 * (start + end + 2 * middle)
            increase = end - start
            return increase / SQRT2, height * SQRT2

    def create_path(self, text, path, color=None):
        """
        Create a path with the given text.

        Parameters
        ----------
        text : str
            texts on the markers.
        path : list[str]
            list of tonal value strings such as ['55','213',...]
        color : str, optional
            This parameter can be any of the following:
                1. Color Name. One of "金茶草柳蔚靛雪墨" designed by unt.
                2. Tonal Name. One of the eight tonal names, each of them corresponds to a unique color name.
                3. Any valid matplotlib color description.
                4. None. Cycle from an iterator created by the eight colors. 
        """
        if color is None:
            color = next(self.color_iter)
        elif color in self.tonal_names:
            color = self.color_map[self.tonal_names.index(color)]
        elif color in self.color_names:
            color = self.color_map[self.color_names.index(color)]
        else:
            color = color
        for i, tonal_value in enumerate(path):
            x, y = self.tonal_value2coord(tonal_value)
            self.create_point(x, y, text, color=color, trans=False)
            
            if i >= 1:
                from_point = self.tonal_value2coord(path[i - 1])
                self.create_arrow_line(
                    from_point,
                    [x, y],
                    color=color,
                    trans=False,
                )
            x_offset,y_offset =-0.5,0
            self.ax.annotate(tonal_value,xy=(x+x_offset, y+y_offset),fontsize=24,color=color,va='center',ha='center')
