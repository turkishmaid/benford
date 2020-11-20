#!/usr/bin/env python
# coding: utf-8

"""
Simple program to iterate thru all files, fetch 1st digit from the
file size and plot the distribution of the different values as
an animated graph.
"""
# Created: 17.11.20


import pygame
import sys
import os
import random
from pathlib import Path
from time import perf_counter


# decorator to support static variables in functions
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@static_vars(_paths=None)
def next() -> int:
    """
    Digit producer. May raise StopIteration when done.
    :return: another digit, value 0..9
    """
    if not next._paths:
        next._paths = Path(os.environ["HOME"]).glob('**/*')
    while True:
        p = next._paths.__next__()
        s = str(p)
        # directories have 96 bytes -> systematic "fraud"
        if not p.is_file():
            continue
        # # many files with lengths like 2*
        # if ".Office/Outlook/" in s:
        #     continue
        # if not "/.git/" in s:
        #     continue
        break
    n = p.stat().st_size
    s = str(n)
    r = int(s[0])
    # if r == 2 and graph.cnt > 200000 and graph.values[2] > graph.values[1]:
    #     print(n, p)
    return r

"""
    without outlook and git files:
              n = 9240
        0 -          2 = 0.000
        1 -       2884 = 0.312
        2 -       1557 = 0.169
        3 -        990 = 0.107
        4 -       1303 = 0.141
        5 -       1110 = 0.120
        6 -        379 = 0.041
        7 -        430 = 0.047
        8 -        347 = 0.038
        9 -        238 = 0.026
    
    all files:
            n = 992493
        0 -       7351 = 0.007
        1 -     265084 = 0.267
        2 -     242976 = 0.245
        3 -     120200 = 0.121
        4 -      90655 = 0.091
        5 -      79231 = 0.080
        6 -      63066 = 0.064
        7 -      46323 = 0.047
        8 -      42172 = 0.042
        9 -      35435 = 0.036
"""

def color(n):
    # https://www.pygame.org/docs/ref/color.html#pygame.Color
    return f"0x{n:06x}"


def random_color() -> pygame.Color:
    """
    Generate a random (but bright) color.
    :return: the Color
    """
    return pygame.Color(random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))


WIDTH = 1000
BARWIDTH = 100  # 10 bars 0..9
HEIGHT = 600


class Graph:
    """
    Simple class to maintaion and pait a bar chart with 10 columns.
    """

    def __init__(self):
        self.cnt = 0
        self.values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pc0 = perf_counter()

    def count(self, x: int) -> None:
        """
        Count an occurence of a digit.
        :param x: the digit
        """
        self.cnt += 1
        self.values[x] += 1

    def paint(self) -> pygame.Surface:
        """
        Paint this Graph.
        :return: a Surface with the painted graph on black background
        """
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill(pygame.Color(0,0,0))
        if self.cnt == 0:
            return
        for x in range(0, 10):
            h = self.values[x] / self.cnt
            top = round(HEIGHT * (1 - h), 0)
            bar = pygame.Rect(BARWIDTH * x, top, BARWIDTH, 5)
            # pygame.draw.rect(surface, pygame.Color(255,255,255), bar)
            pygame.draw.rect(surface, random_color(), bar)
        return surface

    def stat(self):
        print()
        print("n =", self.cnt)
        for i, v in enumerate(self.values):
            print(f"{i} - {v:10d} = {v/self.cnt:.3f}")
        dpc = perf_counter() - self.pc0
        print(f"elapsed ~ {dpc:.1f} s")


def update(graph, n) -> None:
    """
    Process many values into a Graph.
    :param graph: the Graph
    :param n: process that number of values
    """
    for i in range(0, n):
        graph.count(next())
    # print(".", end="", flush=True)


if __name__ == "__main__":
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    FPS = 1
    FramePerSec = pygame.time.Clock()

    INCREMENT = 10000  # iterate that man times per painting of the Graph

    pc0 = perf_counter()
    graph = Graph()
    done = False
    while not done:
        try:
            update(graph, INCREMENT)
        except StopIteration:
            done = True
        except KeyboardInterrupt:
            done = True
        # print(graph.cnt, end=" ", flush=True)  # because it's so tedious to print in a Surface
        surf = graph.paint()
        DISPLAYSURF.blit(surf, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                graph.stat()
                sys.exit()
        FramePerSec.tick(FPS)
    # when done
    pygame.quit()
    graph.stat()
    sys.exit()
