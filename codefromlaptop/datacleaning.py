import pandas as pd
from pandas import DataFrame, concat
import numpy as np
import random as rand


def create_samples(num_samples,seed):
    rand.seed(seed)
    for j in range(num_samples):
        file = pd.read_csv('/Users/elizabethrogers/Desktop/RSRG/GenericBatchFileWithInfo.csv')

        target_file = pd.read_csv('/Users/elizabethrogers/Desktop/RSRG/GenericBatchFileALL.csv')
        # file containing emissions rates for each 
        em_info = pd.read_csv('/Users/elizabethrogers/Desktop/RSRG/StateRatesInfo.csv')


        target_array = target_file.to_numpy()
        
        # store emissions rate constants
        # em_info = em_info.to_numpy()

        # test = target_file

        # save the values necessary for calculating emissions rates
        fuel_type = file['Fuel Type'].to_numpy()
        min_MW = file['Min MW'].to_numpy()
        max_MW = file['Max MW'].to_numpy()
        state = file['stid'].to_numpy()

        # create empty arrays for each rate we want to calculate
        NO2 =[]
        SO2 = []
        PM25 = []
        VOC = []
        MWs = []


        # def calc_rates():
        for i in range(len(fuel_type)):
            # sample random generation amount
            MW = rand.uniform(min_MW[i],max_MW[i])

            MWs.append(MW)


            # print(state[i])
            em = em_info.loc[em_info['State ID'] == state[i], ['Fuel Type','Emissions Type', 'Emissions Rate']]
            em = em.loc[em['Fuel Type'] == fuel_type[i], ['Emissions Type', 'Emissions Rate']].to_numpy()
            
            # print(em)

            NO2.append(MW * em[0][1])
            SO2.append(MW * em[1][1])
            PM25.append(MW * em[2][1])
            VOC.append(MW * em[3][1])

            target_array[i][8] = MW * em[0][1]
            target_array[i][9] = MW * em[1][1]
            target_array[i][12] = MW * em[2][1]
            target_array[i][13] = MW * em[3][1]



            # print(NO2)
            # print(SO2)
            # print(PM25)

            # return

        # insert relevant values
        file.insert(8, 'NOx', NO2) # Insert 'C' at index 1 (second column)
        file.insert(9, 'SO2', SO2) # Insert 'C' at index 1 (second column)
        file.insert(10,'NH3',0*len(NO2))
        file.insert(11,'SOA',[0]*len(NO2))
        file.insert(12, 'PM25', PM25) # Insert 'C' at index 1 (second column)
        file.insert(13, 'VOC', VOC) # Insert 'C' at index 1 (second column)
        file.insert(14, 'MW', MWs)


        # # remove extra rows not in scenario file
        final_file = file.drop('Min MW', axis=1) 
        final_file = final_file.drop('Max MW', axis=1) 
        final_file = final_file.drop('MW', axis=1)
        final_file = final_file.drop('Bus number', axis=1) 
        final_file = final_file.drop('Fuel Type', axis=1)

        final_file.insert(0,'ID', [2]*len(NO2))

        # print(final_file.head())
        # line = DataFrame({"onset": 30.0, "length": 1.3}, index=[3])
        # df2 = concat([df.iloc[:2], line, df.iloc[2:]]).reset_index(drop=True)


        # print(final_file.head())

        # Save the DataFrame to a CSV file
        name1 = 'DataFile' + str(j + 1) + '.csv'
        name1 = 'testDataFile.csv'
        file.to_csv(name1, index=False)


        # target_array = target_array.astype(str)

        # final_target_file = pd.DataFrame(target_array, columns =['ID','typeindx','sourceindx','stid','cyid','TIER1','TIER2','TIER3','NOx','SO2','NH3','SOA','PM25','VOC'])

        final_target_file = pd.concat([final_file, target_file])

        print(final_target_file.head())

        # name = 'Emissions_Scenario' + str(j + 1) + '.csv'
        name = 'testScenario.csv'

        # final_target_file.astype(str)

        final_target_file.to_csv(name,index=False)


def create_batch_file(num_samples):
    with open("batch.txt", "w") as file:
        for i in range(num_samples):
            scenario = "\"C:\\Users\\elrog\\COBR\A\input files\\new data\\ScenarioEmissions\\BatchFile" + str(i+1)+".csv\""
            outcome = "\"C:\\Users\\elrog\\COBRA\\input files\\new data\\Output_080425\\Outcome"+str(i+1)+".csv\""
            file.write("\"C:\\Users\\elrog\\COBRA\\cobra_console.exe\" -d \"C:\\Users\\elrog\\COBRA\\data\\cobra.db\" -b \"C:\\Users\\elrog\\COBRA\\input files\\new data\\Emissions_2023_baseline_data.csv\" -c "+scenario+ "-p \"C:\\Users\\elrog\\COBRA\\input files\\new data\\default_2023_population_data.csv\" -i \"C:\\Users\\elrog\\COBRA\\input files\\default data\\default_2023_incidence_data.csv\" -v \"C:\\Users\\elrog\\COBRA\\input files\\new data\\default_2023_valuation_data.csv\" -o "+outcome+ " --discountrate 2 \n")              

# print("\"C:\\Users\\elrog\\COBRA\\input files\\new data\\ScenarioEmissions\BatchFile.csv\"")
create_samples(200,5)
create_batch_file(200)

