import pandas as pd
from pandas import DataFrame, concat
import numpy as np
import random as rand

def create_samples(num_samples,seed):
    rand.seed(seed)
    print("starting...")

    file = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\GenericBatchFileWithInfo.csv")

    generic_file = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\GenericBatchFileALL.csv")
    # file containing emissions rates for each 
    em_info = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\StateRatesInfo.csv")

    carbon_emi = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\NewEnglandFiles\\Fall116CarbonEmiGeneratorresults.csv")
    low_health = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\NewEnglandFiles\\Fall116LowHealthBoundGeneratorresults.csv")
    high_health = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\NewEnglandFiles\\Fall116HighHealthBoundGeneratorresults.csv")
    mixed_high = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\NewEnglandFiles\\Fall116mixhighGeneratorresults.csv")
    mixed_low = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\NewEnglandFiles\\Fall116mixlowGeneratorresults.csv")
    origional = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\NewEnglandFiles\\Fall116originalGeneratorresults.csv")
    
    
    # target_array = target_file.to_numpy()
    
    # store emissions rate constants
    # em_info = em_info.to_numpy()

    # test = target_file

    # save the values necessary for calculating emissions rates
    fuel_type = file['Fuel Type'].to_numpy()
    state = file['stid'].to_numpy()

    # create empty arrays for each rate we want to calculate
    No2 =[]
    So2 = []
    Pm25 = []
    VoC = []

    # def calc_rates():
    for i in range(6):
        # sample random generation amount
        if(i == 0):
            MW = carbon_emi["Carbon Cost"]
        elif(i==1):
            MW = low_health["Low Health Bound"]
        elif(i==2):
            MW = high_health["High Health Bound"]
        elif(i==3):
            MW = mixed_high["Mixed High Health Bound"]
        elif(i==4):
            MW = mixed_low["Mixed Low Health Bound"]
        else:
            MW = origional["Operational Cost"]


        # print(state[i])
        em = em_info.loc[em_info['State ID'] == state[i], ['Fuel Type','Emissions Type', 'Emissions Rate']]
        em = em.loc[em['Fuel Type'] == fuel_type[i], ['Emissions Type', 'Emissions Rate']].to_numpy()
        
        # print(em)

        No2.append(MW * em[0][1] / 2000)
        So2.append(MW * em[1][1] / 2000)
        Pm25.append(MW * em[2][1] / 2000)
        VoC.append(MW * em[3][1] / 2000)

        # target_array[i][8] = MW * em[0][1] / 2000
        # target_array[i][9] = MW * em[1][1] / 2000
        # target_array[i][12] = MW * em[2][1] / 2000
        # target_array[i][13] = MW * em[3][1] / 2000


        # insert relevant values
        file.insert(8, 'NOx', No2) # Insert 'C' at index 1 (second column)
        file.insert(9, 'SO2', So2) # Insert 'C' at index 1 (second column)
        file.insert(10,'NH3',[0]*len(No2))
        file.insert(11,'SOA',[0]*len(No2))
        file.insert(12, 'PM25', Pm25) # Insert 'C' at index 1 (second column)
        file.insert(13, 'VOC', VoC) # Insert 'C' at index 1 (second column)


        # # remove extra rows not in scenario file
        final_file = file.drop('Min MW', axis=1) 
        final_file = final_file.drop('Max MW', axis=1) 
        final_file = final_file.drop('MW', axis=1)
        final_file = final_file.drop('Bus number', axis=1) 
        final_file = final_file.drop('Fuel Type', axis=1)

        final_file = final_file.insert(0,'ID', [2]*len(No2))

        # print(final_file.head())
        # print(final_file.head())

        # Save DataFrame to a CSV file
        name1 = 'DataFile' + str(i + 1) + '.csv'
        # name1 = 'testDataFile.csv'
        file.to_csv(name1, index=False)


        # target_array = target_array.astype(str)

        # final_target_file = pd.DataFrame(target_array, columns =['ID','typeindx','sourceindx','stid','cyid','TIER1','TIER2','TIER3','NOx','SO2','NH3','SOA','PM25','VOC'])

        final_target_file = pd.concat([final_file, generic_file])

        # print(final_target_file.head())

        name = 'Emissions_Scenario' + str(i + 1) + '.csv'
        # name = 'testScenario.csv'

        # final_target_file.astype(str)

        final_target_file.to_csv(name,index=False)

create_samples()