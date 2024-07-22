import json
from timer import Timer
import numpy as np
from os.path import join
import random
import copy
import os

import shutil
from testcase import TestCase
from aerialist.px4.drone_test import DroneTest
from aerialist.px4.obstacle import Obstacle

from evaluator import Evaluator
from config import CASE_STUDY, RUN, FEATURES
from obstacle_mutator import ObstacleMutator
from folder import Folder
from generation_ai import GPT_object



class Individual(object):
    # Global counter of all the individuals (it is increased each time an individual is created or mutated).
    COUNT = 0
    SEEDS = set()
    COUNT_MISS = 0

    def __init__(self, member1:Obstacle, member2:Obstacle, seed):
        self.id = Individual.COUNT
        self.seed = seed
        self.ff = None
        self.obstacle1 = member1
        self.obstacle2 = member2
        self.features = tuple()
        self.run = RUN
        self.seed = seed
        self.features = FEATURES
        self.tool = "DeepHyperion"
        self.rank = np.inf
        self.selected_counter = 0
        self.placed_mutant = 0
        self.timestamp, self.elapsed_time = Timer.get_timestamps()
        self.test = None

    def reset(self):
        self.ff = None
        self.rank = np.inf
        self.selected_counter = 0
        self.placed_mutant = 0


    def evaluate(self, test_case):
        case_study = DroneTest.from_yaml(test_case)
        self.test = TestCase(case_study, [self.obstacle1, self.obstacle2])
        if self.ff is None:          
            distances = Evaluator.evaluate(self)
            self.ff = distances
        return self.ff

    def mutate(self):
        mutant_num = 0
        mutant_list = []
        mutant_obstacle1 = self.obstacle1
        mutant_obstacle2 = self.obstacle2

        while mutant_num < 5:
            rand = random.randint(0, 1)
            if rand == 0:
                mutant_obstacle1 = ObstacleMutator(self.obstacle1).mutate()
            else:
                mutant_obstacle2 = ObstacleMutator(self.obstacle2).mutate()

            while(mutant_obstacle1.intersects(mutant_obstacle2)):
                if rand == 0:
                    mutant_obstacle1 = ObstacleMutator(self.obstacle1).mutate()
                else:
                    mutant_obstacle2 = ObstacleMutator(self.obstacle2).mutate()

            mutant_list.append([mutant_obstacle1, mutant_obstacle2])
            mutant_num += 1
        
        text_cases = f'''test case 0: (obstacle1: length: {mutant_list[0][0].size.l}, width: {mutant_list[0][0].size.w}, height: {mutant_list[0][0].size.h}, x: {mutant_list[0][0].position.x}, y: {mutant_list[0][0].position.y}, r: {mutant_list[0][0].position.r}; obstacle2: length: {mutant_list[0][1].size.l}, width: {mutant_list[0][1].size.w}, height: {mutant_list[0][1].size.h}, x: {mutant_list[0][1].position.x}, y: {mutant_list[0][1].position.y}, r: {mutant_list[0][1].position.r})\n
        test case 1: (obstacle1: length: {mutant_list[1][0].size.l}, width: {mutant_list[1][0].size.w}, height: {mutant_list[1][0].size.h}, x: {mutant_list[1][0].position.x}, y: {mutant_list[1][0].position.y}, r: {mutant_list[1][0].position.r}; obstacle2: length: {mutant_list[1][1].size.l}, width: {mutant_list[1][1].size.w}, height: {mutant_list[1][1].size.h}, x: {mutant_list[1][1].position.x}, y: {mutant_list[1][1].position.y}, r: {mutant_list[1][1].position.r})\n
        test case 2: (obstacle1: length: {mutant_list[2][0].size.l}, width: {mutant_list[2][0].size.w}, height: {mutant_list[2][0].size.h}, x: {mutant_list[2][0].position.x}, y: {mutant_list[2][0].position.y}, r: {mutant_list[2][0].position.r}; obstacle2: length: {mutant_list[2][1].size.l}, width: {mutant_list[2][1].size.w}, height: {mutant_list[2][1].size.h}, x: {mutant_list[2][1].position.x}, y: {mutant_list[2][1].position.y}, r: {mutant_list[2][1].position.r})\n
        test case 3: (obstacle1: length: {mutant_list[3][0].size.l}, width: {mutant_list[3][0].size.w}, height: {mutant_list[3][0].size.h}, x: {mutant_list[3][0].position.x}, y: {mutant_list[3][0].position.y}, r: {mutant_list[3][0].position.r}; obstacle2: length: {mutant_list[3][1].size.l}, width: {mutant_list[3][1].size.w}, height: {mutant_list[3][1].size.h}, x: {mutant_list[3][1].position.x}, y: {mutant_list[3][1].position.y}, r: {mutant_list[3][1].position.r})\n
        test case 4: (obstacle1: length: {mutant_list[4][0].size.l}, width: {mutant_list[4][0].size.w}, height: {mutant_list[4][0].size.h}, x: {mutant_list[4][0].position.x}, y: {mutant_list[4][0].position.y}, r: {mutant_list[4][0].position.r}; obstacle2: length: {mutant_list[4][1].size.l}, width: {mutant_list[4][1].size.w}, height: {mutant_list[4][1].size.h}, x: {mutant_list[4][1].position.x}, y: {mutant_list[4][1].position.y}, r: {mutant_list[4][1].position.r})\n'''

        init_prompt = ("We are testing an UAV control system. Based on the current state of UAV， you will serve as a predictor to determine which test case "
                   "is the most interesting.\n"
                   "#Current state of UAV\nThe drone will take off from coordinate (0,0), fly to coordinate (45,50), and then fly to coordinate (35,60), and then return to a position where y=0.\n" 
                   "#The definition of interestingness\nIf the obstacles set in the test case could potentially prevent the drone from evading them or if the distance between the drone and the obstacles is less than 1.5, then that test case is considered interesting. \n" 
                   "\n#test cases\n" + text_cases +
                   "#output format\n"
                   "The output should follow these chains of thought: First, analyze the potential flight paths of "
                   "the UAV under each test case (under the heading 'THINKING', all caps). Then Score each test case, with 10 points being the most interesting and 0 points being the least interesting."
                   "All scores will be stored in a list in the order of test case IDs and this list will be outputted (under the heading 'Score List')."
                   "Example for the output: \nTHINKING\n xxxxxxxxxxx "
                   "\n Score List\n [x,x,x,x,x]")

        

        interesting_generation = GPT_object(api_key=os.environ.get("chatGPT_api_key"), init_prompt=init_prompt)

        response = interesting_generation.get_response("Start the analysis")
        print("LLM selected: ", response)

        self.obstacle1 = mutant_list[int(response)][0]
        self.obstacle2 = mutant_list[int(response)][1]
        self.reset()

    def to_dict(self):
        return {'id': str(self.id),
                'seed': str(self.seed),
                'misbehaviour': self.is_misbehavior(),
                'performance': str(self.ff),
                'timestamp': str(self.timestamp),
                'elapsed': str(self.elapsed_time),
                'tool' : str(self.tool),
                'run' : str(self.run),
                'features': self.features,
                'rank': str(self.rank),
                'selected': str(self.selected_counter),
                'placed_mutant': str(self.placed_mutant), 
                'obstacle1': self.obstacle1.to_dict(),
                'obstacle2': self.obstacle2.to_dict()
        }


    def dump(self, filename):
        self.test.save_yaml(filename+".yaml")
        data = self.to_dict()
        filedest = filename+".json"
        with open(filedest, 'w') as f:
            (json.dump(data, f, sort_keys=True, indent=4))
        if self.ff != 10000:
            shutil.copy2(self.test.log_file, f"{filename}.ulg")
            shutil.copy2(self.test.plot_file, f"{filename}.png")

    def is_misbehavior(self):
        if self.ff >= 1.5:
            return False
        else:
            return True

    def export(self, all=False):
        if self.is_misbehavior():
            dst = join(Folder.DST_MIS, "mbr"+str(self.id))
            self.dump(dst)
        if all:
            dst = join(Folder.DST_ALL, "mbr"+str(self.id))
        else:
            dst = join(Folder.DST_ARC, "mbr"+str(self.id))
        self.dump(dst)
