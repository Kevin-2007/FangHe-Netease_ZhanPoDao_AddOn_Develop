import math


def levelToLyMax(level):
    return ((100*math.log10(level))+100) if (level != 0) else 100