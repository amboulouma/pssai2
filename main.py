#Example 1
#Length of the schedule
length_of_schedule = 7

#Number of Employees
number_of_employees = 9

##Number of Shifts
number_of_shifts = 3

# Temporal Requirements Matrix
temporal_requirements_matrix = [
        [2,2,2,2,2,2,2],
        [2,2,2,3,3,3,2],
        [2,2,2,2,2,2,2]
    ]

#ShiftName, Start, Length, MinlengthOfBlocks, MaxLengthOfBlocks
shift_name, start, length, min_length_of_blocks, max_length_of_blocks \
    = ['D', 'A', 'N'], [360, 840, 1320], [480, 480, 480], [2, 2, 2], [7, 6, 4]

# Minimum and maximum length of days-off blocks 
min_days_off = 2
max_days_off = 4 

# Minimum and maximum length of work blocks
min_length_work_blocks = 4
max_length_work_blocks = 7

# Number of not allowed shift sequences: NrSequencesOfLength2, NrSequencesOfLength3: 
nr_sequences_of_length_2 = 3
nr_sequences_of_length_3 = 0

# Not allowed shift sequences 
not_allowed_shif_sequences = [
    ['N', 'D'], ['N', 'A'], ['A', 'D']
]
