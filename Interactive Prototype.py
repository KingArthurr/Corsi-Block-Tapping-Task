# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 10:33:01 2019

@author: Daphne Rietvelt
"""
import sys

STATE = "welcome"
while True:
        if STATE == "welcome":
            print("welcome" )
            input1 = raw_input("What do you want to do?:")
            print (input1)
            if input1 == "next":
                STATE = "questions"
            if input1 == "quit":
                STATE = "quit"
                continue
        
        if STATE == "questions":
            print("questions")
            input2 = raw_input("What do you want to do?:")
            print (input2)
            if input2 == "next":
                STATE = "trial"
                continue
            if input2 == "q":
                STATE = "quit"
            
        if STATE == "trial": 
            print ("trial")
            input3 = raw_input("What do you want to do?:")
            print(input3)
            if input3 == "correctseq":
                STATE = "feedback"
                continue
            if input3 == "incorrectseq":
                STATE = "trial"
                continue
        
        if STATE == "feedback":
            print ("feedback")
            input4 = raw_input("What do you want to do?:")
            print(input3)
            if input4 == "next":
                STATE = "trial"
                continue
            if input4 == "final":
                STATE = "final"
            if input4 == "quit":
                STATE = "quit"
                continue
        
        if STATE == "final":
            print ("final")
            input5 = raw_input("What do you want to do?:")
            print(input5)
            if input5 == "results":
                STATE = "results"
                continue
            if input5 == "save&quit":
                STATE = "quit"
                continue
            
        if STATE == "results":
            print("results")
            input6 = raw_input("What do you want to do?:")
            print(input6)
            if input6 == "back":
                STATE = "final"
        
        if STATE == "quit":
            print ("quit")
            break
sys.exit() 