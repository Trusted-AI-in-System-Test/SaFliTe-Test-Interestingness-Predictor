from typing import List

import pandas as pd
from scipy.stats import qmc
from more_itertools import consecutive_groups

from aerialist.px4.drone_test import DroneTest
from aerialist.px4.obstacle import Obstacle
from shapely.geometry import LineString

from testcase import TestCase
from generation_ai import GPT_object
import os


class Camba(object):
    def __init__(
        self,
        case_study_file: str,
        budget: int,
        num_obstacles: int,
        target_distance: float,
    ) -> None:
        self.case_study = DroneTest.from_yaml(case_study_file)
        self.budget = budget
        self.num_obstacles = num_obstacles
        self.target_distance = target_distance

    def halton_random(self, l_bounds, u_bounds, d=3):
        sampler = qmc.Halton(d=d)
        sample = sampler.random(n=1)
        scaled = qmc.scale(sample, l_bounds, u_bounds)
        return scaled[0]

    def alter_obstacle(
        self,
        obstacle: Obstacle,
        x: float = 0.0,
        y: float = 0.0,
        r: float = 0.0,
        l: float = 0.0,
        w: float = 0.0,
        h: float = 0.0,
    ) -> Obstacle:
        position = Obstacle.Position(
            x=obstacle.position.x + x,
            y=obstacle.position.y + y,
            z=0,
            r=obstacle.position.r + r,
        )
        size = Obstacle.Size(
            l=obstacle.size.l + l,
            w=obstacle.size.w + w,
            h=obstacle.size.h + h,
        )

        return Obstacle(size, position)

    def mutate_gap(self):
        # Mutate closer to each other if gap too large
        obstacles = self.prev_obstacles.copy()
        # Mutate left obstacle
        obstacles[0] = self.alter_obstacle(obstacle=obstacles[0], x=0.3)
        # Mutate right obstacle
        obstacles[1] = self.alter_obstacle(obstacle=obstacles[1], x=-0.3)
        return obstacles

    def mutate_left(self):
        obstacles = self.prev_obstacles.copy()
        # Mutate left obstacle
        obstacles[0] = self.alter_obstacle(obstacle=obstacles[0], x=-1.0)
        # Mutate length and rotation
        if self.drone_up:
            # Obstacle is not too long and rotation within limits
            if obstacles[0].size.l >= 10.5 and obstacles[0].position.r > 10:
                obstacles[0] = self.alter_obstacle(obstacle=obstacles[0], r=-10.0, l=0)
            # Obstacle is not too much rotated and length within limits
            elif obstacles[0].size.l < 10.5 and obstacles[0].position.r <= 10:
                obstacles[0] = self.alter_obstacle(obstacle=obstacles[0], r=0, l=1.5)
            else:
                obstacles[0] = self.alter_obstacle(
                    obstacle=obstacles[0], r=-10.0, l=1.5
                )
        else:
            # Obstacle is not too long and rotation within limits
            if obstacles[0].size.l >= 10.5 and obstacles[0].position.r < 170:
                obstacles[0] = self.alter_obstacle(obstacle=obstacles[0], r=10.0, l=0)
            # Obstacle is not too much rotated and length within limits
            elif obstacles[0].size.l < 10.5 and obstacles[0].position.r >= 170:
                obstacles[0] = self.alter_obstacle(obstacle=obstacles[0], r=0, l=1.5)
            else:
                obstacles[0] = self.alter_obstacle(obstacle=obstacles[0], r=10.0, l=1.5)

        return obstacles[0]

    def mutate_right(self):
        obstacles = self.prev_obstacles.copy()
        # Mutate right obstacle
        obstacles[1] = self.alter_obstacle(obstacle=obstacles[1], x=1.0)
        # Mutate length and rotation
        if self.drone_up:
            # Obstacle is not too long and rotation within limits
            if obstacles[1].size.l >= 10.5 and obstacles[1].position.r < 170:
                obstacles[1] = self.alter_obstacle(obstacle=obstacles[1], r=10.0, l=0)
            # Obstacle is not too much rotated and length within limits
            elif obstacles[1].size.l < 10.5 and obstacles[1].position.r >= 170:
                obstacles[1] = self.alter_obstacle(obstacle=obstacles[1], r=0, l=1.5)
            else:
                obstacles[1] = self.alter_obstacle(obstacle=obstacles[1], r=10.0, l=1.5)
        else:
            # Checks that obstacle is not too long and rotation within limits
            if obstacles[1].size.l >= 10.5 and obstacles[1].position.r > 10:
                obstacles[1] = self.alter_obstacle(obstacle=obstacles[1], r=-10.0, l=0)
            # Checks that obstacle is not too much rotated and length within limits
            elif obstacles[1].size.l < 10.5 and obstacles[1].position.r <= 10:
                obstacles[1] = self.alter_obstacle(obstacle=obstacles[1], r=0, l=1.5)
            else:
                obstacles[1] = self.alter_obstacle(
                    obstacle=obstacles[1], r=-10.0, l=1.5
                )

        return obstacles[1]

    def randomize_obstacle(self):
        # Obstacle size
        l, w, h = self.halton_random(
            l_bounds=[7, 5, 15],
            u_bounds=[12, 8, 25],
        )

        # Obstacle position
        if self.obstacles:
            # Creating second obstacle
            if self.drone_up:
                x, y, r = self.halton_random(
                    l_bounds=[self.point_x, self.point_y - 5, 90],
                    u_bounds=[self.point_x + 3, self.point_y + 5, 180],
                )
            else:
                x, y, r = self.halton_random(
                    l_bounds=[self.point_x, self.point_y - 5, 0],
                    u_bounds=[self.point_x + 3, self.point_y + 5, 90],
                )
        else:
            # Creating first obstacle
            if self.drone_up:
                x, y, r = self.halton_random(
                    l_bounds=[self.point_x - 15, self.point_y - 5, 0],
                    u_bounds=[self.point_x - 5, self.point_y + 5, 90],
                )
            else:
                x, y, r = self.halton_random(
                    l_bounds=[self.point_x - 15, self.point_y - 5, 90],
                    u_bounds=[self.point_x - 5, self.point_y + 5, 180],
                )

        size = Obstacle.Size(l=float(l), w=float(w), h=float(h))
        position = Obstacle.Position(x=float(x), y=float(y), z=0, r=float(r))
        return Obstacle(size, position)

    def create_obstacles(self, mutate=False):
        print("Creating obstacles...")

        if mutate:
            if self.prev_location == 0:
                self.obstacles.append(self.mutate_left())
                self.obstacles.append(self.prev_obstacles[1])
            elif self.prev_location == 1:
                self.obstacles.append(self.prev_obstacles[0])
                self.obstacles.append(self.mutate_right())
            elif self.prev_location == -2:
                self.obstacles = self.mutate_gap().copy()
        else:
            # If not mutate or previous location is -1, create random obstacles
            while len(self.obstacles) < self.num_obstacles:
                is_added = False
                for _ in range(1000):
                    new_obstacle = self.randomize_obstacle()
                    if self.check_obstacles(new_obstacle):
                        self.obstacles.append(new_obstacle)
                        is_added = True
                        break
                # If no combination found, re-randomize obstacle
                if not is_added:
                    self.obstacles = []

    def check_obstacles(self, new_obstacle: Obstacle, min_gap=5.6, max_gap=7.8):
        # Check intersection and gap if there are obstacles
        if self.obstacles:
            for obstacle in self.obstacles:
                # Get distance between two obstacles
                dist = obstacle.distance(new_obstacle.geometry)
                in_gap = min_gap < dist < max_gap
                is_intersect = obstacle.intersects(new_obstacle)
                if is_intersect or not in_gap:
                    return False

        # Check if obstacle is within the bounds of the case study
        min_x, min_y, max_x, max_y = new_obstacle.geometry.bounds
        if min_x < -40 or min_y < 10 or max_x > 30 or max_y > 40:
            return False

        # Check if obstacle is too close or too far to the sample trajectory
        # Get distance between obstacle and sample trajectory
        dist = new_obstacle.distance(self.sample_trajectory)
        in_gap = (min_gap / 2) < dist < (max_gap / 2)
        if in_gap:
            return False

        # Otherwise all checks passed
        return True

    def get_sample_trajectory(
        self,
        min_x=-30,
        min_y=23,
        max_x=20,
        max_y=27,
        num_index=5,
    ):
        """
        df[0]: timestamp
        df[1]: x
        df[2]: y
        df[3]: z
        df[4]: r
        """
        df = pd.DataFrame(self.trajectory.to_data_frame())
        # Select the middle part of the trajectory
        filtered_df = df[
            (df[2] > min_y) & (df[2] < max_y) & (df[1] > min_x) & (df[1] < max_x)
        ]
        # Get a random row from the trajectory
        row = filtered_df.sample()
        # Get the x and y coordinates
        self.point_x = row[1].values[0]
        self.point_y = row[2].values[0]
        # Get the row index
        row_index = row.index[0]
        # Create a sample trajectory
        sample_trajectory = df[row_index - num_index : row_index + num_index]
        points = sample_trajectory.values[:, 1:4]
        self.drone_up = sample_trajectory[2].is_monotonic_increasing
        self.sample_trajectory = LineString(points)

    def get_trajectory_location(self):
        center_points = []
        min_y = 40
        max_y = 10
        for obstacle in self.prev_obstacles:
            min_y = min(min_y, obstacle.geometry.bounds[1])
            max_y = max(max_y, obstacle.geometry.bounds[3])
            center_points.append(obstacle.geometry.centroid.coords[0])

        trajectory_line = self.prev_trajectory.to_line()
        obstacles_line = LineString(center_points)

        # Check if trajectory pass through the gap
        if trajectory_line.intersects(obstacles_line):
            # Return -2 if trajectory pass through the gap
            return -2

        # Select the trajectory in the boundary
        df = pd.DataFrame(self.prev_trajectory.to_data_frame())
        filtered_df = df[
            (df[2] > min_y) & (df[2] < max_y) & (df[1] > -40) & (df[1] < 30)
        ]

        # Select all trajectories that are same direction with drone
        lines: List[LineString] = []
        for rows_index in consecutive_groups(filtered_df.index):
            grouped_df = filtered_df.loc[rows_index]
            points = grouped_df.values[:, 1:4]
            line = LineString(points)
            if self.drone_up and grouped_df[2].is_monotonic_increasing:
                lines.append(line)
            elif not self.drone_up and grouped_df[2].is_monotonic_decreasing:
                lines.append(line)

        # Select the closest trajectory to the obstacles
        closest_dist = float("inf")
        closest_line = None
        for line in lines:
            dist = line.distance(obstacles_line)
            if dist < closest_dist:
                closest_dist = dist
                closest_line = line

        # Check if trajectory is to the left or right of the obstacles
        if closest_line:
            closest_dist = float("inf")
            closest_obstacle_index = None
            for index, obstacle in enumerate(self.prev_obstacles):
                dist = obstacle.distance(closest_line)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_obstacle_index = index
            # Return the index of the closest obstacle
            # 0: left obstacle, 1: right obstacle
            return closest_obstacle_index

        # Return -1 if trajectory cannot be found
        return -1

    def evaluate_test_case(self, save=False) -> TestCase:
        test = TestCase(self.case_study, self.obstacles)

        try:
            trajectory = test.execute()
            if save:
                # Save trajectory for the first iteration
                self.trajectory = trajectory
                self.get_sample_trajectory()
                return

            test.plot()

            # Save all the previous data
            self.prev_trajectory = trajectory
            self.prev_obstacles = self.obstacles.copy()
            self.prev_location = self.get_trajectory_location()

            return test, test.get_distances()

        except Exception as e:
            print("Exception during test execution, skipping the test")
            print("An error occurred: ", type(e).__name__, "-", e)
            # If timeout, return infinity
            self.prev_obstacles = []
            return test, [float("inf")]

    def generate(self) -> List[TestCase]:
        self.test_cases: List[TestCase] = []

        for i in range(self.budget):
            print(f"Generation {i}:")
            self.obstacles: List[Obstacle] = []

            # Get the original trajectory without obstacle
            if not hasattr(self, "trajectory"):
                self.evaluate_test_case(save=True)
                continue

            # Create obstacles
            mutate = (
                True
                if hasattr(self, "prev_obstacles")
                and self.prev_obstacles
                and self.prev_location != -1
                else False
            )
            mutant_list = []
            mutant_num = 0
            while mutant_num < 5:
                self.create_obstacles(mutate=mutate)
                mutant_list.append(self.obstacles)
                mutant_num += 1

            test_cases = ""

            for i, obstacle_list in enumerate(mutant_list):
                test_case_str = f"test case {i}: "
                for j, obstacle in enumerate(obstacle_list):
                    test_case_str += f"(obstacle{j + 1}: length: {obstacle.size.l}, width: {obstacle.size.w}, height: {obstacle.size.h}, x: {obstacle.position.x}, y: {obstacle.position.y}, r: {obstacle.position.r}); "
                test_case_str = test_case_str[:-2] + "\n"
                test_cases += test_case_str

            print("test cases: ", test_cases)

            init_prompt = (
                    "We are testing an UAV control system. Based on the current state of UAV， you will serve as a predictor to determine which test case "
                    "is the most interesting.\n"
                    "#Current state of UAV\nThe drone will take off from coordinate (0,0), fly to coordinate (3,55), and then fly to coordinate (-15,56) return to coordinate (-18,0).\n"
                    "#The definition of interestingness\nIf the obstacles set in the test case could potentially prevent the drone from evading them or if the distance between the drone and the obstacles is less than 1.5, then that test case is considered interesting. \n"
                    "\n#test cases\n" + test_cases +
                    "#output format\n"
                    "The output should follow these chains of thought: First, analyze the potential flight paths of the UAV under each test case and identify the differences between each test case (under the heading 'THINKING', all caps). Then Score each test case, with 10 points being the most interesting and 0 points being the least interesting. The scores cannot all be the same! There must be at least one difference. Consider the differences of each test case, and aim to make the scores of each test case as distinct as possible."
                    "The narrower the predicted path and the sharper the turns, the higher the score. All scores will be stored in a list in the order of test case IDs and this list will be outputted (under the heading 'Score List')."
                    "Example for the output: \nTHINKING\n xxxxxxxxxxx "
                    "\n Score List\n [x,x,x,x,x]")

            interesting_generation = GPT_object(api_key=os.environ.get("chatGPT_api_key"), init_prompt=init_prompt)

            response = interesting_generation.get_response("Start the analysis")
            print("LLM selected: ", response)

            self.obstacles = mutant_list[int(response)]

            # Evaluate test case
            test, distances = self.evaluate_test_case()
            print(f"Distances: {distances}")

            # Reinitialize if hit the target distance
            try:
              if min(distances) < self.target_distance:
                  self.test_cases.append(test)
                  self.prev_obstacles = []
                  self.get_sample_trajectory()
            except (ValueError, SyntaxError):
              print("generate again")

        return self.test_cases
