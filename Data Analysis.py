import matplotlib.pyplot as plt
import statistics
import numpy as np
import csv
import seaborn as sns
from get_data import *
from stats import *
sns.set_theme()

plt.rc('font', size=8)

with open('Carbon Dioxide Emission Estimates.csv', newline='') as csvfile:
    Emi_Reader = csv.DictReader(csvfile)
    Emi_Datalist = []
    for row in Emi_Reader:
        Emi_Datalist.append(row)

with open('Land.csv', newline='') as csvfile:
    Land_Reader = csv.DictReader(csvfile)
    Land_Datalist = []
    for row in Land_Reader:
        Land_Datalist.append(row)

def Country_Data_Check(Emi_Datalist):
    Emissions = []
    Country_In = input("Country >")
    filter_data = list(filter(lambda x: 'Emissions (thousand metric tons of carbon dioxide)' in x.values(), (filter(lambda x: Country_In in x.values(), Emi_Datalist))))
    Year = []
    for x in filter_data:
        Year.append(int(x['Year']))
        Emissions.append(float(x['Value']))
    K, M = Regression_Selector(Year, Emissions, 1970, 2020)
    plt.plot(K, M, color = 'black')
    plt.scatter(Year, Emissions)
    plt.ticklabel_format(style='plain')
    plt.xlabel("Year")
    plt.ylabel("Emissions (thousand metric tons of carbon dioxide)")
    plt.show()
 
def Global_Data_Check(Emi_Datalist):
    Mean_Emi = []
    Dead_Years = []
    Year = Get_Years(Emi_Datalist)
    for Date in np.unique(np.array(Year)):
        Emissions_That_Year = []
        filter_data = list(filter(lambda x: 'Emissions (thousand metric tons of carbon dioxide)' in x.values(), list((filter(lambda x: str(Date) in x.values(), Emi_Datalist)))))
        for x in filter_data:
            Emissions_That_Year.append(float(x['Value']))
        if Emissions_That_Year == []:
            Dead_Years.append(Date)
        else:
            Mean_Emi.append(statistics.mean(Emissions_That_Year))
    Unique_Years = [x for x in np.unique(np.array(Year)) if x not in Dead_Years]
    plt.scatter(Unique_Years, Mean_Emi)
    plt.xlabel("Year")
    plt.ylabel("Mean Global Emissions (thousand metric tons of carbon dioxide)")
    plt.title("Mean Global Emissions Over Time")
    K, M = Regression_Selector(Unique_Years, Mean_Emi, 1970, 2020)
    plt.plot(K, M, color = 'black')
    plt.ticklabel_format(style='plain')
    plt.show()
    Emissions = []
    High_List_Place = []
    High_List_Emi = []
    filter_data = list(filter(lambda x: 'Emissions (thousand metric tons of carbon dioxide)' in x.values(), list(filter(lambda x: "2017" in x.values(), Emi_Datalist))))
    for x in filter_data:
        Emissions.append(float(x['Value']))
        if float(x['Value']) >= 1000000:
            High_List_Place.append(x['Country'])
            High_List_Emi.append(float(x['Value']))
    i = 0
    plt.hist(Emissions, bins=50, histtype='barstacked', color= 'red', edgecolor='black')
    plt.title("Histogram of reported CO2 emissions in 2017")
    plt.xlabel("Emissions (Thousasnd metric tons of CO2) in 2017")
    plt.ylabel("Frequency Density")
    plt.ticklabel_format(style='plain')
    plt.show()
    plt.bar(High_List_Place, High_List_Emi)
    plt.title("Reported CO2 emissions of top polluting countries in 2017")
    plt.xticks(rotation='horizontal')
    plt.xlabel("Country")
    plt.ylabel("Emissions (Thousasnd metric tons of CO2) in 2017s")
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.show()

def Corrolation(Emi_Datalist, Land_Datalist):
    Countries = Get_Countries(Emi_Datalist)
    Land_types = Get_Land(Land_Datalist)
    Emissions_dict = {}
    Emission = []
    Land = []
    for x in Land_types:
        print(x)
    Selected_Land = str(input("Copy and paste the land type you wish to analyze >"))
    Exclusion = str(input("Exclude extreme values? Y or N >"))
    for Country in np.unique(np.array(Countries)):
        filter_emi = list(filter(lambda x: 'Emissions (thousand metric tons of carbon dioxide)' in x.values(), (filter(lambda x: Country in x.values(), filter(lambda x: str('2017') in x.values(), Emi_Datalist)))))
        for x in filter_emi:
            if Exclusion.upper() == "Y":
                if float(x['Value']) > 1500000:
                    pass
                else:
                    Emissions_dict[Country] = float(x['Value'])
            else:
                Emissions_dict[Country] = float(x['Value'])
    for Name, Num in Emissions_dict.items():
        filter_land = list(filter(lambda x: Name in x.values(), filter(lambda x: str('2017') in x.values(), filter(lambda x: Selected_Land in x.values(), Land_Datalist))))
        if filter_land == []:
            pass
        else:
            Emission.append(float(Num))
            Land.append(float(filter_land[0]['Value']))
    Emission = np.array(Emission)
    Land = np.array(Land)
    Corrolation_Coeff = Pearson_correlation(np.array(Land), np.array(Emission))
    print("Corrolation Coefficient = " + str(Corrolation_Coeff))
    plt.scatter(Land, Emission)
    plt.ticklabel_format(style='plain')
    plt.xlabel(str(Selected_Land))
    plt.ylabel("Emissions (Thousasnd metric tons of CO2) in 2017")
    K, M = Regression_Selector(Land, Emission, 0, round(max(Land)))
    plt.plot(K, M, color = 'black')
    bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
    if Corrolation_Coeff < 0:
        plt.text(max(Land, key=lambda x: x), max(Emission, key=lambda x: x) + 0.3, ("Pearson Corrolation Coefficient:" + str(Corrolation_Coeff)), fontsize=9, bbox=bbox, horizontalalignment='right')
    else:
        plt.text(max(Land, key=lambda x: x), min(Emission, key=lambda x: x) + 0.3, ("Pearson Corrolation Coefficient:" + str(Corrolation_Coeff)), fontsize=9, bbox=bbox, horizontalalignment='right')
    plt.title('Emissions in 2017 vs ' + str(Selected_Land))
    plt.show()

Entry = int(input("1 for data by country, 2 for global data, 3 for corrolation"))
if Entry == 1:
    Country_Data_Check(Emi_Datalist)
elif Entry == 2:
    Global_Data_Check(Emi_Datalist)
elif Entry == 3:
    Corrolation(Emi_Datalist, Land_Datalist)
else:
    exit()