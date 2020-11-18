#!/usr/bin/env python
# coding: utf-8

"""
EXPLAIN_WHAT_THIS_IS_ALL_ABOUT_PLEASE
"""
# Created: 17.11.20

import pygame
import sys
import random


# decorator to support static variables in functions
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


# infinite iterator
@static_vars(cnt=0)
def next():
    next.cnt += 1
    return next.cnt


# the function
def f(n):
    s = str(n)
    return int(s[0])


def color(n):
    # https://www.pygame.org/docs/ref/color.html#pygame.Color
    return f"0x{n:06x}"


def random_color():
    return pygame.Color(random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))


WIDTH = 1000
BARWIDTH = 100  # 10 bars 0..9
HEIGHT = 600


class Graph:

    def __init__(self):
        self.cnt = 0
        self.values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def count(self, x):
        self.cnt += 1
        self.values[x] += 1

    def paint(self):
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


def update(graph, n):
    for i in range(0, n):
        graph.count(f(next()))


pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 10
FramePerSec = pygame.time.Clock()

INCREMENT = 10

graph = Graph()
while True:
    update(graph, INCREMENT)
    print(graph.cnt, end=" ", flush=True)
    surf = graph.paint()
    DISPLAYSURF.blit(surf, (0,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    FramePerSec.tick(FPS)