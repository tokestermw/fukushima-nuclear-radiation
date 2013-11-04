# Group by dates while putting a filter for a couple reasons:
# 1. reduce the dataset for interpolation
# 2. reduce the dataset for the maps
# 3. reduce autocorrelation for the interpolation
# 4. provide a way to play with different filters

class Filter:

    def __init__(self, group_type):
        self.group_type = group_type
        pass

    def avg():
        pass

