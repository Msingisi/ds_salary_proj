# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:23:53 2024

@author: mzing
"""

import pandas as pd
import re

df = pd.read_csv('glassdoor_jobs.csv')

#salary parsing

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if '/hr' in x.lower() else 0)

df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].str.replace("The minimum salary range is", "").str.replace("The maximum salary range is", "-")
salary_extract = salary.apply(lambda x: x.split(')')[1]).apply(lambda x: x.replace('K','').replace('$',''))

df['min_salary'] = salary_extract.apply(lambda x: float(x.split('-')[0]))
df['max_salary'] = salary_extract.apply(lambda x: float(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#parsing of job titles

def title_simplifier(title):
    if 'data scientist' in title.lower():
       return 'Data Scientist'
    elif 'data engineer' in title.lower():
       return 'Data Scientist'
    elif 'analyst' in title.lower():
       return 'Analyst'
    elif 'machine learning' in title.lower():
       return 'Mle' 
    elif 'ai' in title.lower():
       return 'AI'
    elif 'manager' in title.lower():
       return 'Manager'
    else:
       return 'Other'
   
df['job_simp'] = df['Job Title'].apply(title_simplifier)
df['job_simp'].value_counts()


df['seniority'] = df['Job Title'].apply(lambda x: 'Senior' if 'senior' in x.lower() or 'sr' in x.lower() else
                        ('Junior' if 'junior' in x.lower() or 'jr' in x.lower() or 'associate' in x.lower() else
                        ('Entry-Level' if 'entry-level' in x.lower() or 'entry level' in x.lower() else
                        ('Mid-Level' if 'mid level' in x.lower() or 'mid-level' in x.lower() else 'Other'))))
#remote jobs

df['remote'] = df['Location'].apply(lambda x: 1 if "remote" in x.lower() else 0)

def extract_state(location):
    try:
        return location.split(',')[1].strip()  # Remove any leading/trailing spaces
    except IndexError:
        return None 

df['job_state'] = df['Location'].apply(extract_state)

#age of company

df['Founded'] = df['Founded'].str.replace("--", "-1")
df['age'] = df['Founded'].apply(lambda x: int(x) if int(x) < 1 else 2024 - int(x))

#parsing of job description(education level, python, etc...)

#bachelor
df['bachelor'] = df['Job Description'].apply(lambda x: 1 if "bachelor's" in x.lower()
                                             or "bachelor" in x.lower() or "bs" in x.lower() else 0)

#masters
df['masters'] = df['Job Description'].apply(lambda x: 1 if "master's" in x.lower() 
                                            or "msc" in x.lower() else 0)

#phd
df['PhD'] = df['Job Description'].apply(lambda x: 1 if "phd" in x.lower() else 0)



#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if "python" in x.lower() else 0)

#sql
df['sql_yn'] = df['Job Description'].apply(lambda x: 1 if "sql" in x.lower() else 0)

#java
df['java_yn'] = df['Job Description'].apply(lambda x: 1 if "java" in x.lower() else 0)

#spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if "spark" in x.lower() else 0)

#power bi
df['power bi_yn'] = df['Job Description'].apply(lambda x: 1 if "power bi" in x.lower() else 0)

#sas
df['sas_yn'] = df['Job Description'].apply(lambda x: 1 if "sas" in x.lower() else 0)

#aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if "aws" in x.lower() else 0)

#excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if "excel" in x.lower() else 0)

#tableau
df['tableau_yn'] = df['Job Description'].apply(lambda x: 1 if "tableau" in x.lower() else 0)

#study field

field_keywords = ["Computer Science", "Statistics", "Mathematics", "Engineering"]

def extract_first_education(job_description):
    for keyword in field_keywords:
        if keyword.lower() in job_description.lower():
            return keyword
    return "Not specified"

df['study_field'] = df['Job Description'].apply(extract_first_education)

df.to_csv('glassdoor_jobs_cleaned.csv', index = False)

dff = pd.read_csv('glassdoor_jobs_cleaned.csv')