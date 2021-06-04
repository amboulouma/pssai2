from pprint import pprint

from utils import *

FILENAME = 'rws_instances/Example1.txt'
input_data = read_data(FILENAME)

# Results Employees per days
result = [['-']*input_data['length_of_schedule']]*input_data['number_of_employees']

for e in range(input_data['number_of_employees']):
    for d in range(input_data['length_of_schedule']):
        result[e][d] = 'D'

pprint(input_data)

pprint(result)  