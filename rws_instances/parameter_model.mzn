%%%%% Input %%%%%

% Minimum number of consecutive shifts
int: minOn;
% Maximum number of consecutive shifts
int: maxOn;
% Minimum number of consecutive free days
int: minOff;
% Maximum number of consecutive free days
int: maxOff;
% Number of employees
int: groups;
% Number of shift types
int: numShifts;
% Array containing the minimum number of consecutive shifts of the corresponding type
array[int] of int: minShift;
% Array containing the maximum number of consecutive shifts of the corresponding type
array[int] of int: maxShift;
% Array containing a set of shifts that are forbidden to follow the corresponding type
array[int] of set of int: forbidden;
% Array of shift sequences of length 3 that are forbidden
array[int,int] of int: forbidden3;
% Matrix of dimension numShifts x 7 indicating the demand of each shift type for each day
array[int,int] of int: demand;