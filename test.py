from unt_plot import UntPlot

# Chongqing Sample
up = UntPlot()
up.create_path(text="阴", path=["44", "55", "45"], color="阴平")
up.create_path(text="阳", path=["11", "21", "31"], color="阳平")
up.create_path(text="上", path=["552", "441", "341"], color="阴上")
up.create_path(text="去", path=["24", "13", "213"], color="阴去")

up.fig.savefig("重庆.png")
