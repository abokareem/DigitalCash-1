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
import pickle


class CustomerClass(object):
    def __init__(self, identity):
        print("Customer oject has been created")
        self.identity = identity
        
    #Create Entie Money Order
    def createMO(self, valueOfMoneyOrder, IDofMO): 

        IDList = []
        with open ('usedIDs.txt', 'rb') as var:
           IDList = pickle.load(var)
        print(IDList)
        uniquenessString = randomInt(100,500)
        while True:
            if uniquenessString in IDList: 
                uniquenessString = randomInt(100,500)
            else: 
                IDList.append(uniquenessString)
                break
            
        #Save UIDs to usedIDs.txt                                                
        with open('usedIDs.txt', 'wb') as var:
            pickle.dump(IDList, var)

        customerID = self.identity
        #Base Money Order Complete
        baseMoneyOrder = []
        baseMoneyOrder.append(valueOfMoneyOrder)
        baseMoneyOrder.append(uniquenessString)
        baseMoneyOrder.append(self.identity)
        #Output Base Money Order 
        baseMOFileName = "BaseMO" + str(IDofMO+1) + ".txt"
        writeFile(baseMOFileName,baseMoneyOrder)

        #Secret Split MO Start
        secretSplitMO = []
        secretSplitMO.append(valueOfMoneyOrder)
        secretSplitMO.append(uniquenessString)
        #Secret Split Twice 
        I11 = getSecretSplitting(self)  
        I12 = getSecretSplitting(self) 
        secretSplit = []
        secretSplit.append(I11)
        secretSplit.append(I12)
        secretSplitMO.append(secretSplit)
        #OutputSSMO 
        secretSplitMOFileName = "SecretSplitMO" + str(IDofMO+1) + ".txt"
        writeFile(secretSplitMOFileName,secretSplitMO)
        #OutputSSN
        secretSplitNumberMOFileName = "PRNG_SS" + str(IDofMO+1) + ".txt"
        writeFile(secretSplitNumberMOFileName,secretSplit)

        #Start of Bit Commitment
        #PRNG_BCn.txt
        BCRawOutput = []
        BCRawOutput =performBitCommitment(I11,I12)
        BCOutput = BCRawOutput[0]
        BCRANDNUMS = BCRawOutput[1]

        R111 = BCRANDNUMS[0]
        R112 = BCRANDNUMS[1]
        R121 = BCRANDNUMS[2]
        R122 = BCRANDNUMS[3]
        S111 = BCRANDNUMS[4]
        S112 = BCRANDNUMS[5]
        S121 = BCRANDNUMS[6]
        S122 = BCRANDNUMS[7]


        randIntBCFileName = "PRNG_BC" + str(IDofMO+1) + ".txt"
        writeFile(randIntBCFileName,secretSplit)
        #BitCommitNumsn.txt
        randIntBCFileName = "BitCommitNums" + str(IDofMO+1) + ".txt"
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
        writeFile(randIntBCFileName,BCNUMS)   

        #BitCommitMOn.txt                       #Do we want to make output into Ciphertext? Yes 
        randIntBCFileName = "BitCommitMO" + str(IDofMO+1) + ".txt"
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
        #BlindedMOn.txt                      #Do we want to make output into Ciphertext? Yes 
        blindedMOFileName = "BlindedMO" + str(IDofMO+1) + ".txt"
        writeFile(blindedMOFileName,blindedMO)

        #Start of Unblinding 
        unblindedMO = unblindMO(blindedMO)
        #UnblindedMOn.txt
        blindedMOFileName = "UnblindedMO" + str(IDofMO+1) + ".txt"
        writeFile(blindedMOFileName,unblindedMO)

        #Start of Reveal
        revealedMO = revealMO(unblindedMO,R11,R111,R112,S11,S111,S112,R12,R121,R122,S12,S121,S122)
        #BitCommitRevealMOn.txt
        revealMOFileName = "BitCommitRevealMO" + str(IDofMO+1) + ".txt"
        writeFile(revealMOFileName,revealedMO)

        #Start of Joining


#START OF CALLED CLASSES 

def revealMO(MO,R11,R111,R112,S11,S111,S112,R12,R121,R122,S12,S121,S122):
    VAR1 = [(R11^R111^R112),R111]
    VAR2 = [(S11^S111^S112),S111]     #Output give you the bank verifies, which should match BitCommitment
    VAR3 = [(R12^R121^R122),R121]
    VAR4 = [(S12^S121^S122),S121]
    returnList = []
    returnList.append(VAR1)
    returnList.append(VAR2)
    returnList.append(VAR3)
    returnList.append(VAR4)
    return returnList

'''
Text file (BitCommitRevealMOn.txt) representing the revealed bit-commited money order
'''

def unblindMO(MO):
    #BANK RSA KEY
    bankKeyE = 29
    bankKeyN = 571
    bankKeyD = 59 
    unblindedMO = []
    #Value
    unblindedMO.append(int(MO[0]) ** bankKeyD % bankKeyN) #Ciphertext number, does output have to be Characters?
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
    #BANK PUBLIC RSA KEY
    bankKeyE = 29
    bankKeyN = 571
    blindedMO = []
    #Value of MO 
    blindedMO.append(int(MO[0]) ** bankKeyE % bankKeyN) #Ciphertext number, does output have to be Characters?
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
    I12S = [(S12^S121^S122),S121]
    outputValue = []
    outputValue.append(I11R)
    outputValue.append(I11S)
    outputValue.append(I12R)
    outputValue.append(I12S)

    outputValue2 = []
    outputValue2.append(R111)
    outputValue2.append(R112)
    outputValue2.append(R121)
    outputValue2.append(R122)
    outputValue2.append(S111)
    outputValue2.append(S112)
    outputValue2.append(S121)
    outputValue2.append(S122)

    returnValue = []
    returnValue.append(outputValue)
    returnValue.append(outputValue2)

    return returnValue

def getSecretSplitting(self):
    R = randomNumberwithLength(len(str(self.identity)))
    S = R ^ self.identity
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


'''
def join(R11,R12):
#This portion needs to match the original MO Amount, Uniqueness String, and Identity Strings

    R11^S11 = Identity, because we really only obfuscated the ID in this step

'''


#Questions
'''
Show how far we've come. 
Where do we go next
Can't reverse the bitcommitment
'''

