import pandas as pd
from pandas import DataFrame, concat
import numpy as np
import random as rand


def create_samples(num_samples,seed):
    rand.seed(seed)
    print("starting...")
    for j in range(num_samples):
        file = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\RTS_generic.csv")

        generic_file = pd.read_csv("C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\GenericBatchFileALL.csv")

        
        # save the values necessary for calculating emissions amounts
        nox = file['NOx Rate'].to_numpy()
        so2 = file['SO2 Rate'].to_numpy()
        pm25 = file['PM25 Rate'].to_numpy()
        voc = file['VOC Rate'].to_numpy()
        min_MW = file['Min MW'].to_numpy()
        max_MW = file['Max MW'].to_numpy()


        # create empty arrays for each emission amount we want to calculate
        No2 =[]
        So2 = []
        Pm25 = []
        VoC = []
        MWs = []


        # def calc_rates():
        for i in range(len(file)):
            # sample random generation amount
            MW = rand.uniform(min_MW[i],max_MW[i])

            MWs.append(MW)


            # calculate and save emissions amouts in tons/hr
            No2.append(MW * nox[i])
            So2.append(MW * so2[i])
            Pm25.append(MW * pm25[i])
            VoC.append(MW * voc[i])

        # drop emissions rate from file
        file = file.drop('NOx Rate',axis=1)
        file = file.drop('SO2 Rate',axis=1)
        file = file.drop('PM25 Rate',axis=1)
        file = file.drop('VOC Rate',axis=1)

        # insert relevant values to save for later
        file.insert(9, 'NOx', No2) # Insert 'C' at index 1 (second column)
        file.insert(10, 'SO2', So2) # Insert 'C' at index 1 (second column)
        file.insert(13, 'PM25', Pm25) # Insert 'C' at index 1 (second column)
        file.insert(14, 'VOC', VoC) # Insert 'C' at index 1 (second column)
        file.insert(15, 'MW', MWs) # generation amount 
        file.insert(0,'ID',[2]*len(file))

        # # remove extra rows not in scenario file
        final = file.drop('Min MW', axis=1) 
        final = final.drop('Max MW', axis=1) 
        final = final.drop('MW', axis=1)
        final = final.drop('Bus ID', axis=1) 
        final = final.drop('Fuel Type', axis=1)\
        



        # print(final_file.head())
        # print(final_file.head())

        # Save DataFrame to a CSV file
        name1 = 'DataFile' + str(j + 1) + '.csv'
        # name1 = 'testDataFile.csv'
        file.to_csv(name1, index=False)


        # target_array = target_array.astype(str)

        # final_target_file = pd.DataFrame(target_array, columns =['ID','typeindx','sourceindx','stid','cyid','TIER1','TIER2','TIER3','NOx','SO2','NH3','SOA','PM25','VOC'])

        final_target_file = pd.concat([final, generic_file])

        # print(final_target_file.head())

        name = 'Emissions_Scenario' + str(j + 1) + '.csv'
        # name = 'testScenario.csv'

        # final_target_file.astype(str)

        final_target_file.to_csv(name,index=False)


# still need to update file paths
def create_batch_file(num_samples, group):
    file_index = 1
    for i in range(int(num_samples / group)):
        filename = "batch"+str(i+1) + ".txt"
        with open(filename, "w") as file:
            for j in range(group):
                # change this
                scenario = "\"C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\EmissionsScenarios\\Scenarios090425\\Emissions_Scenario" + str(file_index)+".csv\""
                outcome = "\"C:\\Users\\Loaner\\Desktop\\COBRA Outcomes\\Experiment 090425\\Outcome"+str(file_index)+".csv\""
                # change baseline file
                baseline = "\"C:\\Users\\Loaner\\Desktop\\powersystemspublichealth\\BatchFileCreationCommands\\Emissions_2023.csv\""
                population = "\"C:\\Users\\Loaner\\COBRA\\input files\\default data\\default_2023_population_data.csv\""
                incidence_data = "\"C:\\Users\\Loaner\\COBRA\\input files\\default data\\default_2023_incidence_data.csv\""
                valuation_data = "\"C:\\Users\\Loaner\\COBRA\\input files\\default data\\default_2023_valuation_data.csv\""
                # filename = "\"C:\\Users\\elrog\\COBRA\\cobra_console.exe\" -d \"C:\\Users\\elrog\\COBRA\\data\\cobra.db\" -b " + baseline + " -c "+scenario+ " -p \"C:\\Users\\elrog\\COBRA\\input files\\new data\\default_2023_population_data.csv\" -i \"C:\\Users\\elrog\\COBRA\\input files\\default_2023_incidence_data.csv\" -v \"C:\\Users\\elrog\\COBRA\\input files\\new data\\default_2023_valuation_data.csv\" -o "+outcome+ " --discountrate 2 \n \n"        

                file.write("\"C:\\Users\\Loaner\\COBRA\\cobra_console.exe\" -d \"C:\\Users\\Loaner\\COBRA\\data\\cobra.db\" -b " + baseline + " -c "+scenario+ " -p " + population + " -i " + incidence_data + " -v " + valuation_data +" -o "+outcome+ " --discountrate 2 \n \n")              
                file_index+=1
                # print(filename)

# print("\"C:\\Users\\elrog\\COBRA\\input files\\new data\\ScenarioEmissions\BatchFile.csv\"")
# create_samples(500,1)
# create_samples(10,0)
# create_samples(800,0)
create_samples(3,0)

