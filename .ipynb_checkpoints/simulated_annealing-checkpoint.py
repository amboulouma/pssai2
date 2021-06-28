#!/usr/bin/env python
# coding: utf-8
# %%

# %%


import random
from pprint import pprint
import math
from copy import deepcopy
import time
import traceback

import numpy as np


# %%


def read_data(filename):
    input_data = {}
    #Length of the schedule
    length_of_schedule = 0

    #Number of Employees
    number_of_employees = 0

    ##Number of Shifts
    number_of_shifts = 0

    # Temporal Requirements Matrix Shifts per Days
    temporal_requirements_matrix = []

    #ShiftName, Start, Length, MinlengthOfBlocks, MaxLengthOfBlocks
    shift_name, start_shift, length_shift, min_length_of_blocks, max_length_of_blocks         = [], [], [], [], []

    # Minimum and maximum length of days-off blocks 
    min_days_off = 0
    max_days_off = 0 

    # Minimum and maximum length of work blocks
    min_length_work_blocks = 0
    max_length_work_blocks = 0

    # Number of not allowed shift sequences: NrSequencesOfLength2, NrSequencesOfLength3: 
    nr_sequences_of_length_2 = 0
    nr_sequences_of_length_3 = 0

    # Not allowed shift sequences 
    not_allowed_shif_sequences = [
        ['N', 'D'], ['N', 'A'], ['A', 'D']
    ]
    with open(filename, 'r') as f:
        lines = iter(f.readlines())
        for line in lines:
            if "#Length of the schedule" in line:
                length_of_schedule = int(next(lines))
            if "#Number of Employees" in line:
                number_of_employees = int(next(lines))
            if "##Number of Shifts" in line:
                number_of_shifts = int(next(lines))
            if "# Temporal Requirements Matrix" in line:
                ns = number_of_shifts
                temporal_requirements_matrix = []
                for i in range(number_of_shifts):
                    temporal_requirements_matrix.append(list(map(int, next(lines).split())))
            if "#ShiftName" in line:
                ns = number_of_shifts
                shift_name, start_shift, length_shift, min_length_of_blocks, max_length_of_blocks                     = ['-']*ns, [0]*ns, [0]*ns, [0]*ns, [0]*ns
                for i in range(number_of_shifts):
                    shift_name[i], start_shift[i], length_shift[i], min_length_of_blocks[i], max_length_of_blocks[i] = next(lines).split()
                    start_shift[i], length_shift[i] = list(map(int, start_shift[i])), list(map(int, length_shift[i]))
                min_length_of_blocks, max_length_of_blocks = [int(x) for x in min_length_of_blocks], [int(x) for x in max_length_of_blocks] 
            if "# Minimum and maximum length of days-off blocks" in line:
                min_days_off, max_days_off = list(map(int, next(lines).split()))
            if "# Minimum and maximum length of work blocks" in line:
                min_length_work_blocks, max_length_work_blocks = list(map(int, next(lines).split()))
            if "# Number of not allowed shift sequences: NrSequencesOfLength2, NrSequencesOfLength3:" in line:
                nr_sequences_of_length_2, nr_sequences_of_length_3 = list(map(int, next(lines).split()))
            if "# Not allowed shift sequences" in line:
                not_allowed_shift_sequences_2, not_allowed_shift_sequences_3 = [], []
                for i in range(nr_sequences_of_length_2):
                    not_allowed_shift_sequences_2.append(next(lines).split('\n')[0].split())
                for i in range(nr_sequences_of_length_3):
                    not_allowed_shift_sequences_3.append(next(lines).split('\n')[0].split())

    input_data = {
        'length_of_schedule': length_of_schedule,
        'number_of_employees': number_of_employees,
        'number_of_shifts': number_of_shifts, 
        'temporal_requirements_matrix': temporal_requirements_matrix,
        'shift_name': shift_name,
        'start_shift': start_shift,
        'length_shift': length_shift,
        'min_length_of_blocks': min_length_of_blocks,
        'max_length_of_blocks': max_length_of_blocks,
        'min_days_off': min_days_off,
        'max_days_off': max_days_off,
        'min_length_work_blocks': min_length_work_blocks,
        'max_length_work_blocks': max_length_work_blocks,
        'nr_sequences_of_length_2': nr_sequences_of_length_2,
        'nr_sequences_of_length_3': nr_sequences_of_length_3,
        'not_allowed_shift_sequences_2': not_allowed_shift_sequences_2,
        'not_allowed_shift_sequences_3': not_allowed_shift_sequences_3    
    }

    return input_data 


# %%


def generate_random_solution(input_data):
    code = input_data['shift_name'] + ['-']
    return [[random.choice(code) for d in range(input_data['length_of_schedule'])] for e in range(input_data['number_of_employees'])]


# %%
def demand_constraint(result, input_data):
    for e in range(input_data['number_of_employees']):
        for d in range(input_data['length_of_schedule']):
            sum_day, sum_afternoon, sum_night = 0, 0, 0
            if result[e][d] == 'D': sum_day += 1
            elif result[e][d] == 'A': sum_afternoon += 1
            elif result[e][d] == 'N': sum_night += 1    
        
        if input_data['number_of_shifts'] > 2 :
            if  sum_day >= input_data['temporal_requirements_matrix'][0][d] and sum_afternoon >= input_data['temporal_requirements_matrix'][1][d] and sum_night >= input_data['temporal_requirements_matrix'][2][d]:
                pass
            else:
                return False
        else:
            if  sum_day >= input_data['temporal_requirements_matrix'][0][d] and sum_afternoon >= input_data['temporal_requirements_matrix'][1][d]:
                pass
            else:
                return False
    return True


# %%
#day off constraint
def day_off_constraint(result, input_data):
    for e in range(input_data['number_of_employees']):
        count_dayoff = 0
        for d in range(input_data['length_of_schedule']):
            if result[e][d] == '-': count_dayoff += 1
        if input_data['min_days_off'] <= count_dayoff <= input_data['max_days_off']: pass
        else: return False
    return True


# %%
#working days in a row constraint
def length_work_blocks_constraint(result, input_data):
    for e in range(input_data['number_of_employees']):
        count_consecutive = 0
        min_flag, max_flag = False, False
        for d in range(input_data['length_of_schedule'] - 1):
            if result[e][d] != '-' and result[e][d+1] != '-': 
                count_consecutive += 1
                if count_consecutive >= input_data['min_length_work_blocks'] - 1:
                    min_flag = True
                    if count_consecutive <= input_data['max_length_work_blocks'] - 1:
                        max_flag = True
            else:  count_consecutive = 0
        if min_flag and max_flag: pass
        else: return False
    return True


# %%

#forbidden shifts constraint
def forbidden_constraint2(result, input_data):
    if input_data['not_allowed_shift_sequences_2'] == []: return True
    if input_data['not_allowed_shift_sequences_2'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 1):
                for f in input_data['not_allowed_shift_sequences_2']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]: return False
        return True


# %%
def forbidden_constraint3(result, input_data):
    if input_data['not_allowed_shift_sequences_3'] == []: return True
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: return False
        return True


# %%
def update_demand_constraint(result, input_data):
    updated_result = deepcopy(result)
    for d in range(input_data['length_of_schedule']):
        sum_day, sum_afternoon, sum_night = 0, 0, 0
        for e in range(input_data['number_of_employees']):
            if updated_result[e][d] == 'D': sum_day += 1
            elif updated_result[e][d] == 'A': sum_afternoon += 1
            elif updated_result[e][d] == 'N': sum_night += 1

        if sum_day >= input_data['temporal_requirements_matrix'][0][d]: pass
        else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'D'
        if sum_afternoon >= input_data['temporal_requirements_matrix'][1][d]: pass
        else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'A'
        if input_data['number_of_shifts'] > 2 :
            if sum_night >= input_data['temporal_requirements_matrix'][2][d]: pass
            else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'N'
    return updated_result


# %%
def move_day_demand_constraint(result, input_data):
    updated_result = deepcopy(result)
    for d in range(input_data['length_of_schedule']):
        sum_day = 0
        for e in range(input_data['number_of_employees']):
            if updated_result[e][d] == 'D': sum_day += 1
        if sum_day >= input_data['temporal_requirements_matrix'][0][d]: pass
        else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'D'
    return updated_result


# %%
def move_afternoon_demand_constraint(result, input_data):
    updated_result = deepcopy(result)
    for d in range(input_data['length_of_schedule']):
        sum_afternoon = 0
        for e in range(input_data['number_of_employees']):
            if updated_result[e][d] == 'A': sum_afternoon += 1
        if sum_afternoon >= input_data['temporal_requirements_matrix'][0][d]: pass
        else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'A'
    return updated_result


# %%
def move_night_demand_constraint(result, input_data):
    updated_result = deepcopy(result)
    for d in range(input_data['length_of_schedule']):
        sum_night = 0
        for e in range(input_data['number_of_employees']):
            if updated_result[e][d] == 'N': sum_night += 1
        if sum_night >= input_data['temporal_requirements_matrix'][0][d]: pass
        else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'N'
    return updated_result

# %%


#day off constraint
def update_day_off_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    for e in range(input_data['number_of_employees']):
        count_dayoff = 0
        for d in range(input_data['length_of_schedule']):
            if updated_result[e][d] == '-': count_dayoff += 1
        if count_dayoff >= input_data['min_days_off']: pass
        else: updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = '-'
        if count_dayoff <= input_data['max_days_off']: pass
        else: updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = random.choice(list(set(code) - set('-')))            
    return updated_result


# %%
#day off constraint
def move_min_day_off_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    for e in range(input_data['number_of_employees']):
        count_dayoff = 0
        for d in range(input_data['length_of_schedule']):
            if updated_result[e][d] == '-': count_dayoff += 1
        if count_dayoff >= input_data['min_days_off']: pass
        else: updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = '-'
    return updated_result


# %%
def move_max_day_off_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    for e in range(input_data['number_of_employees']):
        count_dayoff = 0
        for d in range(input_data['length_of_schedule']):
            if updated_result[e][d] == '-': count_dayoff += 1
        if count_dayoff <= input_data['max_days_off']: pass
        else: updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = random.choice(list(set(code) - set('-')))            
    return updated_result


# %%
#working days in a row constraint
def update_length_work_blocks_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    for e in range(input_data['number_of_employees']):
        count_consecutive = 0
        min_flag, max_flag = False, False
        for d in range(input_data['length_of_schedule'] - 1):
            if updated_result[e][d] != '-' and updated_result[e][d+1] != '-': 
                count_consecutive += 1
                if count_consecutive >= input_data['min_length_work_blocks'] - 1:
                    min_flag = True
                    if count_consecutive <= input_data['max_length_work_blocks'] - 1:
                        max_flag = True
            else:  count_consecutive = 0
                
        if min_flag: pass
        else: 
            count_concecutive = 0
            for d in range(input_data['length_of_schedule']):
                if updated_result[e][d] == '-' and count_concecutive <= input_data['max_length_work_blocks'] - 1: 
                    updated_result[e][d] = random.choice(list(set(code) - set('-')))
                count_concecutive += 1
        if max_flag: pass
        else: updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = '-'
                
    return updated_result 


# %%
def move_length_work_blocks_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    
    updated_result

# %%


# %%
#forbidden shifts constraint
def update_forbidden_constraint2(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_2'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_2'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 1):
                for f in input_data['not_allowed_shift_sequences_2']:
                    if updated_result[e][d] == f[0] and updated_result[e][d+1] == f[1]:
                        for c in code:
                            if [f[0], c] not in input_data['not_allowed_shift_sequences_2']:
                                updated_result[e][d+1] = c
                                break
        return updated_result


# %%
#forbidden shifts constraint
def update_forbidden_constraint2_2(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_2'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_2'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 1):
                for f in input_data['not_allowed_shift_sequences_2']:
                    if updated_result[e][d] == f[0] and updated_result[e][d+1] == f[1]: 
                        for c in code:
                            if [c, f[1]] not in input_data['not_allowed_shift_sequences_2']:
                                updated_result[e][d] = c
                                break
        return updated_result


# %%
def update_forbidden_constraint3(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_3'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: 
                        for c in code:
                            if [c, f[1], f[2]] not in input_data['not_allowed_shift_sequences_3']:
                                updated_result[e][d] = c
                                break
                            
        return updated_result


# %%
def update_forbidden_constraint3_2(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_3'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: 
                        for c in code:
                            if [f[0], c, f[2]] not in input_data['not_allowed_shift_sequences_3']:
                                updated_result[e][d] = c
                                break
                            
        return updated_result


# %%


def eval_solution(solution, input_data):
    score = 0
    c1, c2, c3, c4, c5 = demand_constraint,                          day_off_constraint,                          length_work_blocks_constraint,                          forbidden_constraint2,                          forbidden_constraint3
    if c1(solution, input_data): score += 50
    if c2(solution, input_data): score += 15
    if c3(solution, input_data): score += 15
    if c4(solution, input_data): score += 10
    if c5(solution, input_data): score += 10
    
    return score


# %%


def exp_probability(solution, neighbor, T, input_data):
    return math.exp((eval_solution(neighbor, input_data) - eval_solution(solution, input_data))/T)


# %%


def simulated_annealing(input_data, T_max, r, termination_condition, halting_condition):
    tc = 0
    hc = 0
    score = 100
    T = T_max
    
    solution = generate_random_solution(input_data)
    
    while hc < halting_condition:
        while tc < termination_condition:
            if eval_solution(solution, input_data) == 100: 
                return solution
            
            n1 = update_forbidden_constraint3(solution, input_data)
            n2 = update_forbidden_constraint3_2(solution, input_data)
            n3 = update_forbidden_constraint2(solution, input_data)
            n4 = update_forbidden_constraint2_2(solution, input_data)
            n5 = update_length_work_blocks_constraint(solution, input_data)
            n6 = update_day_off_constraint(solution, input_data)
            n7 = update_demand_constraint(solution, input_data)

            neighborhood = [n1, n2, n3, n4, n5, n6, n7]

            neighbor = random.choice(neighborhood)

            if eval_solution(solution, input_data) < eval_solution(neighbor, input_data): solution = neighbor
            elif random.uniform(0, 1) < exp_probability(solution, neighbor, T, input_data): solution = neighbor
            
            tc += 1
            
        T *= r    
        hc += 1
        
    return "Not satified in the given time", solution


# %%


def eval_SA_params(input_data, T_max, tc_max, hc_max, time_limit):
    print(f"Running SA on {input_data['filename']}")
    params = []
    start_time_limit = time.time()
    for T in range(1, T_max):
        end_time_limit = time.time()
        if end_time_limit - start_time_limit > time_limit:
            break
        for hc in range(1, hc_max):
            end_time_limit = time.time()
            if end_time_limit - start_time_limit > time_limit:
                break
            for tc in range(1, tc_max):
                end_time_limit = time.time()
                if end_time_limit - start_time_limit > time_limit:
                    print(f'Exceeded time limit of {time_limit} seconds.')
                    break
                start = time.time()
                solution = simulated_annealing(input_data, T, 0.99, tc, hc)
                end = time.time()
                if solution != "Not satified in the given time":
                    print(f'Parameters solution T={T}\tr={0.99}\ttermination_condition={tc}\thalting_condition={hc}\tRuntime {end - start}')
                    params.append((T, r/100, tc, hc, end - start))
    return params


# %%


def get_examples():
    RWS_INSTANCES = 'rws_instances/'
    EXAMPLE = 'Example'
    filenames = []

    for i in range(1,21):
        filenames.append(RWS_INSTANCES + EXAMPLE + str(i) + '.txt')
    return filenames


# %%


def run_SA_eval_on_examples():
    T = 100
    tc = 100
    hc = 100
    time_limit = 100
    params = {}
    for example in get_examples():
        input_data = read_data(example)
        input_data['filename'] = example
        params[example] = eval_SA_params(input_data, T, tc, hc, time_limit)
        
    return params


# %%


def run_SA_on_examples():
    T = 100
    r = 0.99
    tc = 1000
    hc = 1000
    solutions = {}
    for example in get_examples():
        solution = simulated_annealing(read_data(example), T, r/100, tc, hc)
        print(example)
        pprint(solution)
        solutions[example] = solution


# %%


def test_reading_input():
    for example in get_examples():
        print(example)
        pprint(read_data(example))


# %%


def test_constraints():
    for example in get_examples():
        print(example)
        solution = generate_random_solution(read_data(example))
        pprint(eval_solution(solution, read_data(example)))


# %%


def test_SA():
    T_max = 100
    r = 0.99
    termination_condition = 1000
    halting_condition = 1000000
    for example in get_examples():
        print(example)
        input_data = read_data(example)
        solution = generate_random_solution(input_data)
        solution = simulated_annealing(input_data, T_max, r, termination_condition, halting_condition)
        if "Not satified in the given time" not in solution:
            print(eval_solution(solution, input_data))
            print('passed')
        else: 
            message, solution = solution
            print(f'{message}. Best solution found has a score of: {eval_solution(solution, input_data)}')
            print('Not passed')
        

