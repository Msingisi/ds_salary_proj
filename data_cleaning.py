# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:23:53 2024

@author: mzing
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')

#salary parsing
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if '/hr' in x.lower() else 0)


df = df[df['Salary Estimate'] != '-1']


salary = df['Salary Estimate'].str.replace("The minimum salary is ", "").str.replace(
    "and the max salary is", " – ").apply(lambda x: x.split('(')[0]).apply(lambda x: x.replace(
        '/hr ','').replace('/yr ','').replace('/mo', '').replace('K','').replace('$', ''))
        

df['min_salary'] = salary.apply(lambda x: float(x.split(' – ')[0]))
df['max_salary'] = salary.apply(lambda x: x.split(' – ')[1]).apply(lambda x: float(x.split('.')[0]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#parsing of job titles

def title_simplifier(title):
    if 'data scientist' in title.lower():
       return 'Data Scientist'
    elif 'engineer' in title.lower():
       return 'Data Engineer'
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

df['seniority'] = df['Job Title'].apply(lambda x: 'Senior' if 'senior' in x.lower() or 'sr' in x.lower() 
        or 'lead' in x.lower() or 'principal' in x.lower() or 'iv' in x.lower() 
        or 'iii' in x.lower() else
        ('Junior' if 'junior' in x.lower() or 'jr' in x.lower() or 'associate' in x.lower() 
         or 'data scientist i' in x.lower() else
        ('Mid-Level' if 'mid level' in x.lower() or 'mid-level' in x.lower() or 'ii' in x.lower() else 'na')))


#remote jobs

df['remote'] = df['Location'].apply(lambda x: 1 if "remote" in x.lower() or 'united states' in x.lower() else 0)

#state name only

def extract_state(location):
    try:
        return location.split(',')[1].strip()  # Remove any leading/trailing spaces
    except IndexError:
        return None 

df['job_state'] = df['Location'].apply(extract_state)
df['job_state'] = df['job_state'].str.replace("Fulton", "GA")

#age of company
df['Founded'] = df['Founded'].str.replace("--", "-1")
df['age'] = df['Founded'].apply(lambda x: int(x) if int(x) < 1 else 2024 - int(x))


#parsing of job description(education level, study field, python, etc...)

#bachelor's
df['bachelors'] = df['Job Description'].apply(lambda x: 1 if "bachelor's" in x.lower()
                                              or "bachelor" in x.lower()
                                              or "bachelors" in x.lower() else 0)

#masters
df['masters'] = df['Job Description'].apply(lambda x: 1 if "master's" in x.lower()
                                            or "masters" in x.lower() else 0)
                                            

#PhD
df['PhD'] = df['Job Description'].apply(lambda x: 1 if "phd" in x.lower() else 0)
                                            

df['PhD'] = df['Job Description'].apply(lambda x: 1 if "phd" in x.lower() else 0)


#statistics
df['statistics'] = df['Job Description'].apply(lambda x: 1 if "statistics" in x.lower() else 0)


#mathematics
df['mathematics'] = df['Job Description'].apply(lambda x: 1 if "mathematics" in x.lower()
                                                or "math" in x.lower() else 0)

#computer Science
df['computer Science'] = df['Job Description'].apply(lambda x: 1 if "computer Science" in x.lower() else 0)


#economics
df['economics'] = df['Job Description'].apply(lambda x: 1 if "economics" in x.lower() else 0)


#python
df['python'] = df['Job Description'].apply(lambda x: 1 if "python" in x.lower() else 0)


#sql
df['sql'] = df['Job Description'].apply(lambda x: 1 if "sql" in x.lower() else 0)


#java
df['java'] = df['Job Description'].apply(lambda x: 1 if "java" in x.lower() else 0)


#R
df['R'] = df['Job Description'].apply(lambda x: 1 if " r " in x.lower() else 0)
df['R'].value_counts()

#spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if "spark" in x.lower() else 0)


#power bi
df['power_bi'] = df['Job Description'].apply(lambda x: 1 if "power bi" in x.lower() else 0)


#sas
df['sas'] = df['Job Description'].apply(lambda x: 1 if "sas" in x.lower() else 0)


#aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if "aws" in x.lower() else 0)


#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if "excel" in x.lower() else 0)


#tableau
df['tableau'] = df['Job Description'].apply(lambda x: 1 if "tableau" in x.lower() else 0)

#study field

field_keywords = ["Computer Science", "Statistics", "Mathematics", "Engineering"]


#replace -- with -1 in other columns(Industry, Sector)

df['Industry'] = df['Industry'].str.replace("--", "-1")
df['Sector'] = df['Sector'].str.replace("--", "-1")

df.to_csv('glassdoor_jobs_cleaned.csv', index = False)