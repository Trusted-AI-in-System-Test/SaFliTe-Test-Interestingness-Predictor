from __future__ import annotations
import copy
from aerialist.px4.obstacle import Obstacle
import logging as log
import random

MUTUPPERBOUND = 5
MUTLOWERBOUND = 2
DELTA_R = 20
MIN_DELTA_R = 10
MUTATIONS_LIST = ["r","x","y", "l", "w"] # , "h"


# (-40<x<30, 10<y<40)
    
class ObstacleMutator(object):
    
    def __init__(self, obstacle: Obstacle) -> None:
        super().__init__()
        self.obstacle = obstacle

    def mutate(self) -> Obstacle:
        border  = random.choice(MUTATIONS_LIST)
        if border == "r":
            delta = random.uniform(MIN_DELTA_R, DELTA_R)
        else:
            delta = random.uniform(MUTLOWERBOUND, MUTUPPERBOUND)
        print(f"border: {border}")
        print(f"delta: {delta}")    
        mutant_obstacle = self.move_border(self.obstacle, border, delta)
        while (
            mutant_obstacle.size.l < 2
            or mutant_obstacle.size.w < 2
            or mutant_obstacle.size.h < 15
            or -40 > mutant_obstacle.position.x 
            or mutant_obstacle.position.x > 30
            or 10 > mutant_obstacle.position.y 
            or mutant_obstacle.position.y > 40
        ):
            mutant_obstacle = self.move_border(self.obstacle, border, delta)

        return mutant_obstacle

    def move_border(self, obstacle: Obstacle, border: str, delta: float) -> Obstacle:
        l = obstacle.size.l
        w = obstacle.size.w
        h = obstacle.size.h
        x = obstacle.position.x
        y = obstacle.position.y
        r = obstacle.position.r
        rand = random.randint(0,1)
        if rand == 0:
            if border == "l":
                l += delta
            if border == "w":
                w += delta
            # if border == "h":
            #     h += delta
            if border == "x":
                x += delta
            if border == "y":
                y += delta
            if border == "r":
                r += delta
        else:
            if border == "l":
                l -= delta
            if border == "w":
                w -= delta
            # if border == "h":
            #     h -= delta
            if border == "x":
                x -= delta
            if border == "y":
                y -= delta
            if border == "r":
                r -= delta

        mutant_obstacle = Obstacle(Obstacle.Size(l,w,h), Obstacle.Position(x,y,0,r))

        return mutant_obstacle