from pprint import pprint

from utils import *

FILENAME = 'rws_instances/Example1.txt'
input_data = read_data(FILENAME)

days    = input_data['length_of_schedule']
ne      = input_data['number_of_employees']
ns      = input_data['number_of_shifts']
demand  = input_data['temporal_requirements_matrix']
sn      = input_data['shift_name']
ss      = input_data['start_shift']
ls      = input_data['length_shift']
min_ls  = input_data['min_length_of_blocks']
max_ls  = input_data['max_length_of_blocks']
min_do  = input_data['min_days_off']
max_do  = input_data['max_days_off']
min_lw  = input_data['min_length_work_blocks']
max_lw  = input_data['max_length_work_blocks']
nf2     = input_data['nr_sequences_of_length_2']
nf3     = input_data['nr_sequences_of_length_3']
f2      = input_data['not_allowed_shift_sequences_2']
f3      = input_data['not_allowed_shift_sequences_3']

shifts = ns + 1
day, afternoon, night, dayoff = 1, 2, 3, 4
code = sn + ['-']

def demand_constraint(result):
    for e in range(ne):
        for d in range(days):
            if demand[1][d] > sum([x == 'D' for x in result]):
                pass
    return None

def calculate_result(input_data):
    result = [['-']*days]*ne

    for e in range(ne):
        for d in range(days):
            result[e][d] = 'D'

    demand_constraint(result)

    return result

pprint(input_data)

pprint(calculate_result(input_data))