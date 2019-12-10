'''
Customer 
Created by Noah Smith and Zach Cook 12/7/19.

Usage of Program: 
python3 Customer.py
'''

#Library Imports
import sys
import random
import hashlib

#Customer's Personal Information:
identity = 15
personalInformation = "Alice Cash, 1234 Fake Rd, Howell MI 48843, SSN:102-25-9853"

#Request The Number of Money Orders to Generated
numOfMoneyOrders = int(input("How many money orders should be generated?: "))

def main(): 
    for i in range(numOfMoneyOrders): 
        print("Computing Money Order: ", i + 1)
        valueOfMoneyOrder = float(randomInt(1,500))
                                                        #Round Value of MO to 2 decimal places 
        uniquenessString = randomInt(100000,500000)
                                                        #Add Logic to Not Have Duplicate Unique Strings - TBD later 
        customerID = identity
        #Base Money Order Complete
        baseMoneyOrder = []
        baseMoneyOrder.append(valueOfMoneyOrder)
        baseMoneyOrder.append(uniquenessString)
        baseMoneyOrder.append(identity)
        #Output Base Money Order 
        baseMOFileName = "BaseMO" + str(i+1) + ".txt"
        writeFile(baseMOFileName,baseMoneyOrder)

        #Secret Split MO Start
        secretSplitMO = []
        secretSplitMO.append(valueOfMoneyOrder)
        secretSplitMO.append(uniquenessString)
        #Secret Split Twice 
        I11 = getSecretSplitting()  
        I12 = getSecretSplitting() 
        secretSplit = []
        secretSplit.append(I11)
        secretSplit.append(I12)
        secretSplitMO.append(secretSplit)
        #OutputSSMO 
        secretSplitMOFileName = "SecretSplitMO" + str(i+1) + ".txt"
        writeFile(secretSplitMOFileName,secretSplitMO)
        #OutputSSN
        secretSplitNumberMOFileName = "PRNG_SS" + str(i+1) + ".txt"
        writeFile(secretSplitNumberMOFileName,secretSplit)

        #Start of Bit Commitment
        #PRNG_BCn.txt
        BCOutput = []
        BCOutput =performBitCommitment(I11,I12)
        randIntBCFileName = "PRNG_BC" + str(i+1) + ".txt"
        writeFile(randIntBCFileName,secretSplit)
        #BitCommitNumsn.txt
        randIntBCFileName = "BitCommitNums" + str(i+1) + ".txt"
        R11 = I11[0]
        S11 = I11[1]
        R12 = I12[0]
        S12 = I12[1]
        I11R = BCOutput[0]
        I11S = BCOutput[1]
        I12R = BCOutput[2]
        I12S = BCOutput[3]
        BCNUMS = []
        BCNUMS.append([R11,I11R[0]])
        BCNUMS.append([S11,I11S[0]])
        BCNUMS.append([R12,I12R[0]])
        BCNUMS.append([S12,I12S[0]])
        writeFile(randIntBCFileName,BCNUMS)                #Is this R11 and R111?? 
        #BitCommitMOn.txt                                       #Do we want to make output into Ciphertext? Yes 
        randIntBCFileName = "BitCommitMO" + str(i+1) + ".txt"
        BitCommitMO = []
        BitCommitMO.append(valueOfMoneyOrder)
        BitCommitMO.append(uniquenessString)
        BitCommitMO.append(I11[0])
        BitCommitMO.append(I11[1])
        BitCommitMO.append(I12[0])
        BitCommitMO.append(I12[1])
        writeFile(randIntBCFileName,BitCommitMO)

        #Start Of Blinding 
        blindedMO = blindMO(BitCommitMO)
        #BlindedMOn.txt                                      #Do we want to make output into Ciphertext? Yes 
        blindedMOFileName = "BlindedMO" + str(i+1) + ".txt"
        writeFile(blindedMOFileName,blindedMO)

        #Start of Unblinding 
        unblindedMO = unblindMO(blindedMO)
        #UnblindedMOn.txt
        blindedMOFileName = "UnblindedMO" + str(i+1) + ".txt"
        writeFile(blindedMOFileName,unblindedMO)

def unblindMO(MO):
     #BANK RSA KEY
    bankKeyE = 29
    bankKeyN = 571
    bankKeyD = 59 
    unblindedMO = []
    #Value
    unblindedMO.append(float(MO[0]) ** bankKeyD % bankKeyN) #Ciphertext number, does output have to be Characters?
    #Uniqueness
    unblindedMO.append(int(MO[1]) ** bankKeyD % bankKeyN) #Enhancement: Convert Numbers to Characters
    #I11R
    unblindedMO.append(int(MO[2]) ** bankKeyD % bankKeyN)
    #I11S
    unblindedMO.append(int(MO[3]) ** bankKeyD % bankKeyN)
    #I12R
    unblindedMO.append(int(MO[4]) ** bankKeyD % bankKeyN)
    #I12S
    unblindedMO.append(int(MO[5]) ** bankKeyD % bankKeyN)
    return unblindedMO


def blindMO(MO):
    #BANK RSA KEY
    bankKeyE = 29
    bankKeyN = 571
    bankKeyD = 59 
    blindedMO = []
    #Value
    blindedMO.append(float(MO[0]) ** bankKeyE % bankKeyN) #Ciphertext number, does output have to be Characters?
    #Uniqueness
    blindedMO.append(int(MO[1]) ** bankKeyE % bankKeyN) #Enhancement: Convert Numbers to Characters
    #I11R
    blindedMO.append(int(MO[2]) ** bankKeyE % bankKeyN)
    #I11S
    blindedMO.append(int(MO[3]) ** bankKeyE % bankKeyN)
    #I12R
    blindedMO.append(int(MO[4]) ** bankKeyE % bankKeyN)
    #I12S
    blindedMO.append(int(MO[5]) ** bankKeyE % bankKeyN)
    return blindedMO


def performBitCommitment(I11,I12):
    #0=R    1=S
    R11 = I11[0]
    S11 = I11[1]
    R12 = I12[0]
    S12 = I12[1]
    
    #Generate More Random Numbers
    R111 = randomNumberwithLength(len(str(R11)))
    R112 = randomNumberwithLength(len(str(R12)))
    R121 = randomNumberwithLength(len(str(R11)))
    R122 = randomNumberwithLength(len(str(R12)))
    S111 = randomNumberwithLength(len(str(S11)))
    S112 = randomNumberwithLength(len(str(S12)))
    S121 = randomNumberwithLength(len(str(S11)))
    S122 = randomNumberwithLength(len(str(S12)))
    

    #BC Money Order
    I11R = [(R11^R111^R112),R111]
    I11S = [(S11^S111^S112),S111]
    I12R = [(R12^R121^R122),R121]
    I12S = [(S12^S121^S122),R121]
    outputValue = []
    outputValue.append(I11R)
    outputValue.append(I11S)
    outputValue.append(I12R)
    outputValue.append(I12S)
    return outputValue

def getSecretSplitting():
    R = randomNumberwithLength(len(str(identity)))
    S = R ^ identity
    returnList = [R,S]
    return(returnList)

#Custom Methods for Easy Data Export
def randomNumberwithLength(length):
    lower = 10**(length-1)
    upper = 10**length - 1
    return random.randint(lower, upper)

    
def writeFile(fileName,outputList):  
    outFile = open(fileName,"w")                 
    for value in outputList:
        outFile.write(str(value)+ '\n')
    outFile.close()

def randomInt(min,max):
    randomNumber = random.randint(min,max)
    return int(randomNumber)

main()