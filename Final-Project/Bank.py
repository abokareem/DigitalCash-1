'''
Bank 
Created by Noah Smith and Zach Cook 12/7/19.
'''

import random

#Bank Keys
bankKeyE = 29
bankKeyN = 571
bankKeyD = 59 

class BankClass(object):
    def __init__(self):
        print("Bank oject has been created")
    
    def blindSignatureProtocol(self, orderNumber):
        moneyOrder = []
        fileName = "BlindedMO" + str(orderNumber) + ".txt"
        with open(fileName) as inputfile:
            for line in inputfile:
                moneyOrder.append(line.strip())
        valueofMO = moneyOrder[0]
        uniqueness = moneyOrder[1]
        I11R = int(moneyOrder[2])
        I11S = int(moneyOrder[3])
        I12R = int(moneyOrder[4])
        I12S = int(moneyOrder[5])
        returnMO = []
        #Value of Money Order
        returnMO.append(int(valueofMO)**bankKeyD%bankKeyN)
        returnMO.append(int(uniqueness)**bankKeyD%bankKeyN)
        returnMO.append(int(I11R)**bankKeyD%bankKeyN)
        returnMO.append(int(I11S)**bankKeyD%bankKeyN)
        returnMO.append(int(I12R)**bankKeyD%bankKeyN)
        returnMO.append(int(I12S)**bankKeyD%bankKeyN)
        print(returnMO)
