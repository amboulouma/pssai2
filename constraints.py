from pprint import pprint

from utils import *

FILENAME = 'rws_instances/Example1.txt'
input_data = read_data(FILENAME)

days    = input_data['length_of_schedule']
ne      = input_data['number_of_employees']
ns      = input_data['number_of_shifts']
trm     = input_data['temporal_requirements_matrix']
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

# def 

def calculate_result(input_data):
    result = [['-']*input_data['length_of_schedule']]*input_data['number_of_employees']

    for e in range(input_data['number_of_employees']):
        for d in range(input_data['length_of_schedule']):
            result[e][d] = 'D'

    return result

pprint(input_data)

pprint(calculate_result(input_data))  