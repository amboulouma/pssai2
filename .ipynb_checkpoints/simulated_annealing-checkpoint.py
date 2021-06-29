#!/usr/bin/env python
# coding: utf-8
# %%
import random
from pprint import pprint
import math
from copy import deepcopy
import time
import traceback

import numpy as np

from moves import *
from constraints import *
from utils import *
from evaluation import *


# %%
def generate_random_solution(input_data):
    code = input_data['shift_name'] + ['-']
    return [[random.choice(code) for d in range(input_data['length_of_schedule'])] for e in range(input_data['number_of_employees'])]


# %%
def exp_probability(solution, eval_function, neighbor, T, input_data):
    return math.exp((eval_function(neighbor, input_data) - eval_function(solution, input_data))/T)


# %%
def simulated_annealing(input_data, eval_function, T_max, r, termination_condition, halting_condition):
    tc = 0
    hc = 0
    score = 100
    T = T_max
    
    solution = generate_random_solution(input_data)
    best_solution = deepcopy(solution)
    
    while hc < halting_condition:
        while tc < termination_condition:
            if eval_function(solution, input_data) == 100: 
                print(f'params: T_max={T_max}, r={r}, termination_condition={termination_condition}, halting_condition={halting_condition}')
                return solution, best_solution

            moves = [
                move_day_demand_constraint,
                move_afternoon_demand_constraint,
                move_night_demand_constraint,
                move_min_day_off_constraint,
                move_max_day_off_constraint,
                move_min_length_work_blocks_constraint,
                move_max_length_work_blocks_constraint,
                move_0_forbidden_constraint2,
                move_1_forbidden_constraint2,
                move_0_forbidden_constraint3,
                move_1_forbidden_constraint3,
                move_2_forbidden_constraint3,
                move_all_demand_constraint,
                move_all_day_off_constraint,
                move_all_length_work_blocks_constraint,
                move_all_0_forbidden_constraint2,
                move_all_1_forbidden_constraint2,
                move_all_0_forbidden_constraint3,
                move_all_1_forbidden_constraint3,
                move_all_2_forbidden_constraint3,
            ]

            move = random.choice(moves)(solution, input_data)

            if eval_function(solution, input_data) < eval_function(move, input_data): solution = move
            elif random.uniform(0, 1) < exp_probability(solution, eval_function, move, T, input_data): solution = move
            
            if eval_function(solution, input_data) > eval_function(best_solution, input_data):
                best_solution = deepcopy(solution)
            tc += 1
            
        T *= r    
        hc += 1
        
    return "Not satified in the given time", solution, best_solution


# %%
def test_SA(T_max, r, termination_condition, halting_condition, show_non_optimal):
    best_solutions = []
    for example in get_examples():
        if show_non_optimal:
            print(example)
        input_data = read_data(example)
        solution = generate_random_solution(input_data)
        solution = simulated_annealing(input_data, T_max, r, termination_condition, halting_condition)
        if "Not satified in the given time" not in solution:
            if not show_non_optimal:
                print(example)
            solution, best_solution = solution
            best_solutions.append((example, best_solution, eval_function(best_solution, input_data)))
            print(f'Best solution: {eval_function(best_solution, input_data)}')
            print(f'Last solution: {eval_function(solution, input_data)}')
            print('passed')
            print()
        else: 
            if show_non_optimal:
                message, solution, best_solution = solution
                best_solutions.append((example, best_solution, eval_function(best_solution, input_data)))                
                print(f'{message}. Best solution found has a score of: {eval_function(best_solution, input_data)}')
                print(f'Last solution: {eval_function(solution, input_data)}')
                print('passed')
                print()
    return best_solutions


# %%
def test_SA_per_example(example, eval_function, T_max, r, termination_condition, halting_condition, show_non_optimal):
    if show_non_optimal:
        print(example)
    input_data = read_data(example)
    solution = generate_random_solution(input_data)
    best_solution = generate_random_solution(input_data)
    solution = simulated_annealing(input_data, eval_function, T_max, r, termination_condition, halting_condition)
    if "Not satified in the given time" not in solution:
        if not show_non_optimal:
            print(example)
        solution, best_solution = solution
        best_solutions.append((example, best_solution, eval_function(best_solution, input_data)))
        print(f'Best solution: {eval_function(best_solution, input_data)}')
        print(f'Last solution: {eval_function(solution, input_data)}')
        print('passed')
        print()
    else: 
        if show_non_optimal:
            message, solution, best_solution = solution
            print(f'{message}. Best solution found has a score of: {eval_function(best_solution, input_data)}')
            print(f'Last solution: {eval_function(solution, input_data)}')
            print('passed')
            print()
    return best_solution
