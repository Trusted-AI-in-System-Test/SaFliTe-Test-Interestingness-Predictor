import math
import random
import datetime
import logging
from typing import List
from scenarioState import ScenarioState
from testcase import TestCase
import sys
import os
from generation_ai import GPT_object


class Node:
    def __init__(self, state: ScenarioState, parent):
        self.state = state
        self.parent = parent
        self.visits = 0
        self.reward = 0.0
        self.children = []

    def __str__(self):
        return f"state: \n {str(self.state)}, visits: {self.visits}, reward: {self.reward}"


class MCTS:
    def __init__(self, case_study_file: str)-> None:
        self.initial_state = ScenarioState(case_study_file)
        self.root = Node(self.initial_state, None)

        # hyperparameters for UCB1 and progressive widening
        self.exploration_rate = 1 / math.sqrt(2)
        self.C = 0.5
        self.alpha = 0.5
        self.C_list = [0.4, 0.5, 0.6, 0.7]

        self.test_cases = []

    def select(self, node: Node):
        while not node.state.is_terminal():
            layer = len(node.state.scenario)
            # progressive widening
            if len(node.children) <= self.C_list[layer] * (node.visits ** self.alpha):
                return self.expand(node)
            else:
                node = self.best_child(node)

        return node

    @staticmethod
    def expand(node: Node):
        mutant_num = 0
        mutant_list = []
        node_list = []
        tried_children_state = [c.state for c in node.children]

        while mutant_num < 5:
            new_state = node.state.next_state()
            while new_state in tried_children_state and not new_state.is_terminal():
                new_state = node.state.next_state()


            if len(node.state.scenario) == len(new_state.scenario):
                return None
            else:
                new_node = Node(new_state, node)
                node_list.append(new_node)
                obstacle_list = new_node.state.scenario
                mutant_list.append(obstacle_list)
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
                "#Current state of UAV\nThe drone will take off from coordinate (0,0), fly to coordinate (45,50), and then fly to coordinate (35,60), and then return to a position where y=0.\n"
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

        new_node = node_list[int(response)]


        node.children.append(new_node)
        return new_node

    def simulate(self, state):
        return state.get_reward()

    @staticmethod
    def back_propogate(node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent

    def search(self):
        node = self.select(self.root)
        if node is not None:
            reward, min_distance, test_case = self.simulate(node.state)
            # delete the node if it is invalid
            if reward == 0.0 and len(node.state.scenario) != 0:
                node.parent.children.remove(node)
                node.parent = None

            if 0 <= abs(min_distance) <= 1.5:
                self.test_cases.append(test_case)

            self.back_propogate(node, reward)

    def generate(self, budget: int) -> List[TestCase]:
        reward, distance, test_case = self.simulate(self.root.state)
        self.back_propogate(self.root, reward)
        for i in range(budget):
            self.search()
        return self.test_cases

    def best_child(self, node):
        # UCB1
        return max(node.children, key=lambda child: child.reward / child.visits +
                                             self.exploration_rate * math.sqrt(2 * math.log(node.visits) / child.visits))


if __name__ == '__main__':
    pass



