import random
from os.path import join
from pathlib import Path
import copy
# local imports
from exploration import Exploration
from folder import Folder
from mapelites import MapElites
from features import compute_angle, compute_distance, compute_height
from feature_dimension import FeatureDimension
from individual import Individual
from config import CASE_STUDY, FEATURES, NUM_EXEC
import config
import utils
from aerialist.px4.obstacle import Obstacle

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Load the dataset.




class MapElitesUAV(MapElites):
    min_size = Obstacle.Size(5, 5, 15)
    max_size = Obstacle.Size(20, 20, 25)
    min_position = Obstacle.Position(-20, 15, 0, 0)
    max_position = Obstacle.Position(20, 30, 0, 180)

    def __init__(self, *args, **kwargs):
        super(MapElitesUAV, self).__init__(*args, **kwargs)

    def map_x_to_b(self, x):
        """
        Map X solution to feature space dimensions
        :param x: individual
        :return b: tuple of indexes, cell of the map
        """
        b = tuple()
        for ft in self.feature_dimensions:
            i = ft.feature_descriptor(self, x)
            if i < ft.min:
                ft.min = i
            if i >= ft.bins:
                ft.bins = i
            b = b + (i,)
        return b

    def performance_measure(self, x):
        """
        Apply the fitness function to individual x
        :param x: individual
        :return performance: fitness of x
        """
        # "calculate performance measure"    
        performance = x.evaluate(self.mission)
        # TODO: collect all the inputs generated in this run
        Exploration.add_explored(x)
        return performance

    def mutation(self, x):
        """
        Mutate the solution x
        :param x: individual to mutate
        :return x: mutated individual
        """
        # "apply mutation"
        Individual.COUNT += 1
        obstacle1 = copy.deepcopy(x.obstacle1)
        obstacle2 = copy.deepcopy(x.obstacle2)
        ind = Individual(obstacle1, obstacle2, x.seed)
        ind.mutate()
        return ind

    def generate_random_solution(self):
        """
        To ease the bootstrap of the algorithm, we can generate
        the first solutions in the feature space, so that we start
        filling the bins
        """
        # "Generate random solution"
        # (-40<x<30, 10<y<40)
        Individual.COUNT += 1
        seed = Individual.COUNT
        size = Obstacle.Size(
                l=random.uniform(self.min_size.l, self.max_size.l),
                w=random.uniform(self.min_size.w, self.max_size.w),
                h=random.uniform(self.min_size.h, self.max_size.h),
            )
        position = Obstacle.Position(
            x=random.uniform(self.min_position.x, self.max_position.x),
            y=random.uniform(self.min_position.y, self.max_position.y),
            z=0,
            r=random.uniform(self.min_position.r, self.max_position.r),
        )
        obstacle1 = Obstacle(size, position)

        size = Obstacle.Size(
            l=random.uniform(self.min_size.l, self.max_size.l),
            w=random.uniform(self.min_size.w, self.max_size.w),
            h=random.uniform(self.min_size.h, self.max_size.h),
        )
        position = Obstacle.Position(
            x=random.uniform(self.min_position.x, self.max_position.x),
            y=random.uniform(self.min_position.y, self.max_position.y),
            z=0,
            r=random.uniform(self.min_position.r, self.max_position.r),
        )
        obstacle2 = Obstacle(size, position)
        while(obstacle1.intersects(obstacle2)):
            size = Obstacle.Size(
                l=random.uniform(self.min_size.l, self.max_size.l),
                w=random.uniform(self.min_size.w, self.max_size.w),
                h=random.uniform(self.min_size.h, self.max_size.h),
            )
            position = Obstacle.Position(
                x=random.uniform(self.min_position.x, self.max_position.x),
                y=random.uniform(self.min_position.y, self.max_position.y),
                z=0,
                r=random.uniform(self.min_position.r, self.max_position.r),
            )
            obstacle1 = Obstacle(size, position)

            size = Obstacle.Size(
                l=random.uniform(self.min_size.l, self.max_size.l),
                w=random.uniform(self.min_size.w, self.max_size.w),
                h=random.uniform(self.min_size.h, self.max_size.h),
            )
            position = Obstacle.Position(
                x=random.uniform(self.min_position.x, self.max_position.x),
                y=random.uniform(self.min_position.y, self.max_position.y),
                z=0,
                r=random.uniform(self.min_position.r, self.max_position.r),
            )
            obstacle2 = Obstacle(size, position)

        individual = Individual(obstacle1, obstacle2, seed)

        return individual

    def generate_feature_dimensions(self):
        fts = list()

        if "Distance" in FEATURES:
            # feature 1: distance between two obstacles
            ft1 = FeatureDimension(name="Distance", feature_simulator="compute_distance", bins=1)
            fts.append(ft1)

        if "Height" in FEATURES:
            # feature 2: height difference between two obstacles
            ft2 = FeatureDimension(name="Height", feature_simulator="compute_height", bins=1)
            fts.append(ft2)

        if "Angle" in FEATURES:
            # feature 3: angle difference between two obstacles
            ft3 = FeatureDimension(name="Angle", feature_simulator="compute_angle", bins=1)
            fts.append(ft3)

        return fts

    def feature_simulator(self, function, x):
        """
        Calculates the value of the desired feature
        :param function: name of the method to compute the feature value
        :param x: genotype of candidate solution x
        :return: feature value
        """
        if function == 'compute_distance':
            return compute_distance(x)
        if function == 'compute_height':
            return compute_height(x)
        if function == 'compute_angle':
            return compute_angle(x)

def main():
    # for UAV
    Path("results/logs").mkdir(parents=True, exist_ok=True)
    # Generate random folder to store result
    log_dir_name = Folder.DST
    # Ensure the folder exists
    Path(log_dir_name).mkdir(parents=True, exist_ok=True)

    log_to = f"{log_dir_name}/logs.txt"
    debug = f"{log_dir_name}/debug.txt"

    # Setup logging
    utils.setup_logging(log_to, debug)
    print("Logging results to " + log_to)

    config.to_json(Folder.DST)

    map_E = MapElitesUAV(case_study_file=CASE_STUDY, budget=NUM_EXEC, logs=True)
    map_E.run()

    Individual.COUNT = 0

    print("Exporting inputs ...")
    for uav in Exploration.all_inputs:
        uav.export(all=True)
    


if __name__ == "__main__":
    main()
