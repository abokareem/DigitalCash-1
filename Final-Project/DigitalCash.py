'''
Digital Cash
Created by Noah Smith and Zach Cook 12/7/19.

Usage of Program: 
python3 DigitalCash.py 
'''

#Team Created Classes
import Customer
import Bank

identity = int(input("Please enter your ID: "))
numOfMoneyOrders = int(input("How many money orders would you like to make today?: "))
valueofMO = []

#Start of Program
Alice = Customer.CustomerClass(identity=identity)
Bob = Bank.BankClass()

for i in range(numOfMoneyOrders):
    inputVal = int(input("What is the value of the Money Order " + str((i+1)) + "?: "))
    valueofMO.append(inputVal)

for i in range(numOfMoneyOrders):
    Alice.createMO(valueOfMoneyOrder=valueofMO[i],IDofMO=i)

Bob.blindSignatureProtocol(1)