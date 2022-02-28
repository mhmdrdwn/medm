import csv
import os.path
import timeit
import copy
from datetime import datetime

import numpy as np
import random
import pandas as pd
import numpy  as np

from algorithms import *


def write_header(columns, write_file):
    """
    This function writes header to file
    
    Parameters:
    -----------
    columns: list
        list of strings

    write_file: string
        name of the output file 

    """
    with open(write_file,'w') as run_time_file:
        writer = csv.writer(run_time_file)
        writer.writerow(columns)


def write_run_time(data_to_write, write_file):
    """
    This function writes data to file, It takes list contains
    name of the algorithm, list length, case type, number of 
    iteration, date time recording 

    Parameters:
    -----------
    data_to_write: list
       list of algorithm, length of list...etc

    write_file: string
        name of the file
    """
    with open(write_file, 'a') as run_time_file:
        writer = csv.writer(run_time_file, delimiter=',')
        writer.writerows(data_to_write)


def sort_run_time(list_length, algorithms, cases):
    """
    The function calls calculate_run_time function for 
    each case and each list length
    
    """

    np.random.seed(12235)
    gen_data = np.random.uniform(size=100)
    for case in cases:
        for len_list in list_length:
            if case == 'sorted_case': 
                test_data = sorted(gen_data[:len_list])
            elif case == 'reverse_case': 
                test_data = sorted(gen_data[:len_list],
                        reverse=True)
            else:
                test_data = gen_data[:len_list]
            
            for algorithm in algorithms:
                calculate_run_time(algorithm, test_data, 
                        len_list, case)


def calculate_run_time(algorithm, test_data, 
                       len_list, case):
    """
    The function calculate the time required to 
    run the test, and call save_run_time function 
    to save the data
    
    """
    
    clock = timeit.Timer(stmt = 'sort_func(copy(data))' ,
        globals = {'sort_func': algorithm,
            'data': test_data,
            'copy': copy.copy})
    n_ar, t_ar = clock.autorange()
    run_time_list = np.array(clock.repeat(repeat=7, 
        number=n_ar)) / n_ar

    for num_of_rep, run_time in enumerate(run_time_list):
        save_run_time(algorithm, len_list, case, 
                run_time, num_of_rep)

        
def save_run_time(algorithm, len_list, case, run_time, num_of_rep):
    """ 
    the function save all the data to csv
     
    """
    if algorithm.__name__ == 'sort':
        write_run_time([['numpy_'+ algorithm.__name__, len_list, 
            case, run_time, num_of_rep + 1, datetime.now()]], 
            '../data/all_data.csv')
    elif algorithm.__name__ == 'sorted':
        write_run_time([['python_sort', len_list, case, run_time, 
            num_of_rep + 1, datetime.now()]], 
            '../data/all_data.csv')
    else: 
        write_run_time([[algorithm.__name__, len_list, case, 
            run_time, num_of_rep + 1, datetime.now()]], 
            '../data/all_data.csv')


def clean_data(input_file, output_file, list_length, algorithms, cases):
    """
    The function take all recorded data from input file and
    save the minimum run times to another file ready for plot
    
    """
    all_data = pd.read_csv(input_file, delimiter = ',')
    algorithms = ['merge_sort', 'combined_sort', 'lamport_sort', 
            'quick_sort', 'numpy_sort', 'python_sort', 
            'insertion_sort', 'bubble_sort']
    output_list = []
    for len_list in list_length:
        output_list.append(len_list)
        for algorithm in algorithms:
            for case in cases:
                data = all_data[all_data.list_length == len_list]
                data = data[data.sort_type == algorithm]
                data = data[data.case == case]
                run_time_df = pd.DataFrame(data, columns=['run_time'])
                min_value = np.min(run_time_df)
                output_list.append(min_value.run_time)
        write_run_time([output_list], output_file)
        output_list = []


if __name__ == "__main__":
    write_header(['sort_type', 'list_length', 'case', 'run_time', 
        'number_of_repeats','date_time'], '../data/all_data.csv')
    list_length = range(100000, 1000001, 50000)
    algorithms = [merge_sort, combined_sort, lamport_sort,
            quick_sort, np.sort, sorted, insertion_sort,
            bubble_sort]
    cases = ['sorted_case', 'reverse_case', 'random_case']

    sort_run_time(list_length, algorithms, cases)
    write_header(['list_length', 'merge_sorted', 'merge_reverse',
        'merge_random', 'combined_sorted', 'combined_reverse', 
        'combined_random', 'lamport_sorted', 'lamport_reverse',
        'lamport_random', 'quick_sorted', 'quick_reverse', 
        'quick_random', 'np_sorted', 'np_reverse', 'np_random',
        'py_sorted','py_reverse','py_random', 'insertion_sorted',
        'insertion_reverse', 'insertion_random', 'bubble_sorted', 
        'bubble_reverse', 'bubble_random'],'../data/clean_data.csv')
    clean_data('../data/all_data.csv', '../data/clean_data.csv', 
            list_length, algorithms, cases)
