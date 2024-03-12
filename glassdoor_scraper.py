# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 19:12:14 2024

author: Kenarapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/united-states-data-scientist-jobs-SRCH_IL.0,13_KO14,28.htm?typedKeyword=data%2520scientist&locT=&locId="
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[data-loading="false"]').click()
        except ElementClickInterceptedException:
            pass

        time.sleep(5)

        try:
            driver.find_element(By.CLASS_NAME, "CloseButton").click()  #clicking to the X.
            print('x out worked')
        except NoSuchElementException:
            print('x out failed')
            
        
        #Going through each job in this page
        job_buttons = driver.find_elements(By.XPATH,'//li[@class="JobsList_jobListItem__wjTHv"]')  #jl for Job Listing. These are the buttons we're going to click.
        print("Job buttons:", job_buttons)
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(5)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH, '//div[@class="JobDetails_jobDetailsHeader__Hd9M3"]').text.strip()
                    location = driver.find_element(By.XPATH, '//div[@class="JobDetails_location__mSg5h"]').text
                    job_title = driver.find_element(By.CLASS_NAME, "heading_Level1__FG5gb").text
                    job_description = driver.find_element(By.CLASS_NAME, "JobDetails_jobDetailsSection__y_xa6").text.strip()
                    collected_successfully = True
                except:
                    time.sleep(15)

            try:
                salary_estimate = driver.find_element(By.CLASS_NAME, "SalaryEstimate_salaryEstimateContainer__GkgnI").text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element(By.ID,"rating-headline").text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."
                
            try:
               size = driver.find_element(By.XPATH, '//div[@class="JobDetails_overviewItem__cAsry"]//span[text()="Size"]//following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                size = -1
                
            try:
                founded = driver.find_element(By.XPATH, '//div[@class="JobDetails_overviewItem__cAsry"]//span[text()="Founded"]//following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                founded = -1
                
            try:
                type_of_ownership = driver.find_element(By.XPATH, '//div[@class="JobDetails_overviewItem__cAsry"]//span[text()="Type"]//following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                type_of_ownership = -1
                
            try:
                industry = driver.find_element(By.XPATH, '//div[@class="JobDetails_overviewItem__cAsry"]//span[text()="Industry"]//following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                industry = -1
                
            try:
                sector = driver.find_element(By.XPATH, '//div[@class="JobDetails_overviewItem__cAsry"]//span[text()="Sector"]//following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                sector = -1
                
            try:
                revenue = driver.find_element(By.XPATH, '//div[@class="JobDetails_overviewItem__cAsry"]//span[text()="Revenue"]//following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                revenue = -1
                
            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                #headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                #competitors = -1

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
                #print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                #print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            #try:
                #driver.find_element(By.CLASS_NAME, "site-header-companies").click() 
        

                #try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    #headquarters = driver.find_element(By.CLASS_NAME,'//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                #except NoSuchElementException:
                    #headquarters = -1              

                #try:
                    #competitors = driver.find_element(By.XPATH,'//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                #except NoSuchElementException:
                    #competitors = -1

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            #"Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #"Competitors" : competitors})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[data-test="load-more"]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
#This line will open a new chrome window and start the scraping.