#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:48:43 2018

@author: alec
"""

import os
from subprocess import run

def iterate_submit_dir(root_dir='.'):
    for sub_dir, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'BOUT.inp':
                submit(sub_dir)

def submit(path_to_dir):
    submit_script = ['#!/bin/bash\n', 
                     '#SBATCH --time=24:00:00\n', 
                     '#SBATCH --nodes=1 --ntasks-per-node=48 --cpus-per-task=1\n',
                     '#SBATCH --partition=skl_fua_prod\n',
                     '#SBATCH --account=FUA32_SOLF\n',
                     '#SBATCH --job-name=HESEL\n',
                     ' \n',
                     'mpirun -np 48 ./hesel -q -d ' + path_to_dir + ' \n'
                     ]
    with open('submit_script', 'w') as file:
        file.writelines(submit_script)
    
    run('sbatch submit_script')
    
    os.remove('submit_script')