#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 15:27:23 2021

@author: william
"""

# Import Packages:
import os
import numpy
import pandas as pd

# Define Classes:

class Metric:
    
    def kgConvert(self, lbs = 1):
        kg = lbs / 2.2
        return kg
    
    def selectkg(self, string, num):
        options = ['kg', 'lb']
        if string == options[1]:
            return self.kgConvert(num)
        else:
            return num
    
    def meterConvert(self, ft = 0, inch = 0):
        ft = ft * 0.305
        inch = inch * 0.025
        meters = round(ft + inch, 3)
        return meters
    
    def cmConvert(self, mt = 0, cm = 0):
        mt = mt
        cm = cm / 100
        return cm + mt
        
    def selectft(self, num1, num2, string):
        options = ['m/cm', 'ft/in']
        if string == options[0]:
            return self.cmConvert(num1, num2)
        else:
            return self.meterConvert(num1, num2)
    
class BMI:
    
#    bmi_const = 10000
    m = Metric()
    
    def bmiCalc(self, weight, height):
        bmi = round((weight/(height**2)), 1)
        return bmi
    
    
class Percent:
    
    m = 16.2
    w = 5.4
    
    def perCalc(self, bmi, age, sex = 0):
        temp_fat = (1.2*bmi) + (0.23 * age)
        fat = 0
        if sex > 0:
            fat = temp_fat - self.w
        else:
            fat = temp_fat - self.m
        return round(fat, 2)
    
    def determineSex(self, string):
        options = ['M','W']
        string = string.upper()
        if string == options[0]:
            return 0
        else:
            return 1
    
class Files:
    
    current_folder = os.getcwd()
    val_folder = current_folder + '/Vals/'
    health_df = pd.DataFrame()
    groups = []
    
    
    def createTable(self, file_dir):
        health_table = pd.read_csv(file_dir)
        return health_table

    def createDF(self):
        df_ls = []
        for subdir, dirs, files in os.walk(self.val_folder):
            for file in files:
                df_ls.append(self.createTable(self.val_folder + file))
        self.groups = [i[0:2] for i in files]
        self.health_df = pd.concat(df_ls, axis = 0, keys = self.groups)
        return self.health_df
    
    def sex_selector(self, sex):
        if sex > 0:
            return  self.health_df.loc[self.health_df['Sex'] == 'Female']
        else:
            return self.health_df.loc[self.health_df['Sex'] == 'Male']
       
    def age_selector(self, age, df):
        df = df.reset_index(drop = True)
        df['Age'] = self.groups
        if age <= 40:
            return df.loc[df['Age'] == '20']
        elif age > 40 and age <= 60:
            return df.loc[df['Age'] == '40']
        else:
            return df.loc[df['Age'] == '60']
        
    def health_results(self, bmi, df):
        del df['Sex']
        del df['Age']
        bmi_ls = list(df.iloc[0])
        if bmi >= bmi_ls[2]:
            return 'Over Weight'
        elif bmi <= bmi_ls[0]:
            return 'Under Weight'
        else:
            return 'Healthy Weight'
        
    def process_bmi(self, bmi, age, sex):
        sex_df = self.sex_selector(sex)
        age_df = self.age_selector(age, sex_df)
        return self.health_results(bmi, age_df)

# Free Functions:
        
def selector(string):
    vals = ['Y', 'YES']
    string = string.upper()
    return string in vals

### Define Some instances:
m = Metric()
bmi = BMI()
p = Percent()
f = Files()


### Logic
run_const = True
f.createDF()

# Intro
print('Hello\n', 'Welcome to the BMI and Body Fat Percentage Calculator\n', "Let's get started!")

# Simple loop to keep things moving
while(run_const):
    print("How much do you weigh?")
    weight = int(input("Enter either kg or lb: "))
    weight_selection = input("Is that in kg or lb? ")
    weight = m.selectkg(weight_selection, weight)
    print("How tall are you?" )
    h_num_1 = int(input("Enters only meters or ft first: "))
    h_num_2 = int(input("Now enter only cm or in: "))
    height_selection = input("Is that in m/cm or ft/in? ")
    height = m.selectft(h_num_1, h_num_2, height_selection)
    customer_bmi = bmi.bmiCalc(weight, height)
    print("Your BMI is: ", str(customer_bmi))
    if selector(input("Would you like to know your percent body fat [y/n]? ")):
        age = int(input("How old are you [years]? "))
        sex = p.determineSex(input("What is your sex [m/f]? "))
        per_fat = p.perCalc(customer_bmi, age, sex)
        print("Your Percent Body Fat is: ", str(per_fat), "%")
        if selector(input("Would you like to know if that is healthy [y/n]? ")):
            weight_category = f.process_bmi(customer_bmi, age, sex)
            print('Your weight category is: ', weight_category)
    if selector(input('Would you like to continue[y/n]? ')):
        run_const = True
    else:
        run_const = False # Make sure this can end    

