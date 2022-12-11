#### -*- coding: utf-8 -*-
#### Author: Amit Prakash
#### Note: Some of the variable names should be changed to be shorter. 
#### Also, the file path of the input file needs to be changed.
#### This file solves the knapsack problem with hospitals with Covid-19 cases (limiting the scenario with 3 hospitals in top 10 counties)
"""
Created on Tue Apr 12 08:47:14 2022

@file: Covid Python Project.py
@author: Amit Prakash
"""

#### All necessary libraries/imports are here.
#### Let's import the proper library for type-hinting functions.
from typing import Callable
#### Let's import the proper library for dataframes and related input/output (i/o) for files.
import pandas as pd
#### Let's import the proper library for combinations between the top 10 counties.
import itertools as itertools

### This is the main class, all the code and functionality will be in this class for the program.
class main:

    ## Based on given input files from the problem, we will write a data frame with the top 10 counties and cases.
    ## This function will have 3 variables for the data obtained/translated from different dataframes or the input file.
    ## Parameters: None, all necessary values are read via i/o methods from the pandas library.
    ## Returns: top10Counties: (pd.DataFrame)- The dataframe with the top 10 counties in New York with the most Covid-19 cases.  
    def top10Counties() -> pd.DataFrame:
        # Input/Output Files are read here
        data = pd.read_csv("NYcovidData.txt")
        data.columns = ["Case ID", "Gender", "Age", "County"]

        # Sorting after groupby() & count()
        groupedDF = data.groupby('County').count()

        # Sorting group on descending order
        groupedDF = groupedDF.sort_values('Age', ascending = False)[0:10]

        # Adjusting the data frame appropriately for output to std.out (Standard Output)
        groupedDF.pop('Age')
        groupedDF.pop('Gender')
        top10Counties = groupedDF.rename(columns = {"Case ID": "Total Cases By County"})
        top10Counties.index.name = ''
        top10Counties.columns.name = 'County'

        # Using print to display the top 10 counties to std.out (Standard Output)
        print("Top 10 Covid-19 Cases By County in New York\n\n")
        print(top10Counties)
        return(top10Counties)

    ## Based on a given function, we will save a data frame with the top 10 counties and cases from the function and calculate the best combination of 3 counties for the 3 hospitals.
    ## This function will have 3 variables for the data obtained/translated from different dataframes or the input file.
    ## Parameters: None, all necessary values are read via i/o methods from the pandas library.
    ## Returns: top10Counties: (pd.DataFrame)- The dataframe with the top 10 counties in New York with the most Covid-19 cases.  
    def hospitalLocationFinder(top10Counties: Callable) -> None:

        # Using top10Counties() to define the top10Counties dataframe, so we can use the data frame to choose a location for the 3 hospitals ot build.
        top10Counties = top10Counties()

        # A dictionary displaying the table of counties covered by hospitals in each county.
        d = {
             'C1': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             'C2': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             'C3': [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
             'C4': [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
             'C5': [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
             'C6': [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
             'C7': [0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
             'C8': [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
             'C9': [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
             'C10': [0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
            }

        # An empty list for the values of the top 10 counties with the most Covid-19 cases in New York.
        top10CountiesValues = list()
        # Initialize the list by iterating through the values in the dataframe and adding to the end of the list via append().
        for caseValue in top10Counties.values:
            top10CountiesValues.append(caseValue[0])
            
        # Define lists to be used in the for loop.
        # Output list of cases per combinations of hospital counties.
        totalCasesPerCombinationsOfHospitalCounties = list()
        # Loop list of combinations of hospital counties using itertools.combinations().
        combinationsOfHospitalCounties = list(itertools.combinations(d.keys(), 3))
        # Declare a loop to iterate through each combination of hospital counties.
        for combinationOfHospitalCounties in combinationsOfHospitalCounties:
            # Initialize variables for use throughout the loop.
            # Make a dictionary with the current combination of hospital counties and corresponding cases.
            currentCombinationsWithCases = { list(combinationOfHospitalCounties)[0]: d[list(combinationOfHospitalCounties)[0]],
                                             list(combinationOfHospitalCounties)[1]: d[list(combinationOfHospitalCounties)[1]],
                                             list(combinationOfHospitalCounties)[2]: d[list(combinationOfHospitalCounties)[2]]
                                           }
            # A variable to keep track of the sum of the cases for the current combination of hospital counties.
            currentCombinationsWithCasesSum = 0
            # Another loop for each county inside the combination of cases.
            for hospitalCounty in currentCombinationsWithCases:
                # Yet another loop for each county covered inside the county where the hospital would be.
                for count in range(10):
                    # If the county we are looking at is covered, add its case count to our sum.
                    if(currentCombinationsWithCases[hospitalCounty][count] == 1):
                        currentCombinationsWithCasesSum += top10CountiesValues[count]
            # Add the sum of the cases for the current combination of hospital counties to the end of the list of cases per combinations of hospital counties using append().
            totalCasesPerCombinationsOfHospitalCounties.append(currentCombinationsWithCasesSum)

        # Initialize variables to values from the end of each list.
        # Index of the maximum value is set to the last index of the list (list size (len()) - 1).
        indexOfMaximumValue = len(totalCasesPerCombinationsOfHospitalCounties) - 1
        # The maximum value is set to the value at the last index of the list (list size (len()) - 1).
        maximumValueOfList = totalCasesPerCombinationsOfHospitalCounties[len(totalCasesPerCombinationsOfHospitalCounties) - 1]
        # Create a for loop to iterate over all of the list (up to its size (len()) - 1 
        for count in range(len(totalCasesPerCombinationsOfHospitalCounties) - 1):
            # If the total cases we are looking at in the list is greater than the maximum value we set it as the new maximum value and its index as the new index of the maximum value.
            if(totalCasesPerCombinationsOfHospitalCounties[count] > maximumValueOfList):
                maximumValueOfList = totalCasesPerCombinationsOfHospitalCounties[count]
                indexOfMaximumValue = count
                
        # The ranks (top x out 10 counties in New York) of the best combinations of the counties found, using int() and str()
        # to cast between different data types for ease of use while accessing county names from top10Counties.
        bestCountyRanks = [int(str(combinationsOfHospitalCounties[indexOfMaximumValue][0])[1]),
                           int(str(combinationsOfHospitalCounties[indexOfMaximumValue][1])[1]),
                           int(str(combinationsOfHospitalCounties[indexOfMaximumValue][2])[1])]
        # We now print out the result of the places where the hospitals should be built, using str() and lower() for data formatting purposes.
        print("\n\nHospitals should be opened in " + str(top10Counties.index[bestCountyRanks[0] - 1])[0] + str(top10Counties.index[bestCountyRanks[0] - 1])[1:].lower() + ", " +
              str(top10Counties.index[bestCountyRanks[1] - 1])[0] + str(top10Counties.index[bestCountyRanks[1] - 1])[1:].lower() + ", and " +
              str(top10Counties.index[bestCountyRanks[2] - 1])[0] + str(top10Counties.index[bestCountyRanks[2] - 1])[1:].lower() +
              " counties to serve a maximum number of " + str(maximumValueOfList)[:2] + "," + str(maximumValueOfList)[2:] +
              " Covid-19 cases out of all other possible combinations of counties.\n\n")
        
    # Run the final method for all output for the program to the console for the end-user(s).
    hospitalLocationFinder(top10Counties)
