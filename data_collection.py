# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:19:43 2024

@author: Msingisi
"""

import glassdoor_scraper as gs
import pandas as pd

path = "C:/Users/mzing/Documents/ds_salary_proj/chromedriver.exe"

df = gs.get_jobs('data scientist', 1000, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index =False)