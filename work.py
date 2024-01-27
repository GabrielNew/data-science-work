import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from google.colab import files

class MyFile:

  def readFile(self, nameOfFile):
    upload = files.upload()
    data = pd.read_excel(nameOfFile)
    data = self.cleanFile(data)
    return data
  
  def cleanFile(self, originalData):
    self.originalData = originalData
    self.originalData.drop(self.originalData[self.originalData['Município'] 
                                             == '-'].index, inplace = True)
    self.originalData.drop(self.originalData[self.originalData['Fabricante'] 
                                             == '-'].index, inplace = True)
    return self.originalData

initialFile = MyFile()
dataReturn = initialFile.readFile('vacinas.xlsx')
print(dataReturn)

class Statistics:

  statesBrazil = ('AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT',
                  'MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO',
                  'RR','SC','SP','SE','TO')
  
  IBGEcodes = (280030,150140,310620,140010,530010,500270,510340,
               410690,420540,230440,520870,250750,160030,270430,
               130260,240810,172100,431490,110020,261160,120040,
               330455,292740,211130,355030,221100,320530)

  def __init__(self, initials, mainData):
    self.initials = initials
    self.mainData = mainData

  @property
  def initials(self):
    return self._initials

  @initials.setter
  def initials(self, value):
    self._initials = self.checkState(value)

  @property
  def mainData(self):
    return self.__mainData

  @mainData.setter
  def mainData(self, value):
    self.__mainData = value

  def checkState(self, nameOfState):
    return nameOfState.upper() if (nameOfState.upper() in self.statesBrazil) else False

  def totalFirstShot(self):
    return self.mainData['Dose 1'].sum()

  def totalSecondShot(self):
    return self.mainData['Dose 2'].sum()
  
  def totalShotesInOneState(self):
    if (self.checkState(self.initials)):
      return self.mainData[self.mainData['UF'] == self.initials]['Doses Aplicadas'].sum()
    else:
      return print('Please, select a valid state')

  def countyWithMostDose2(self):
    df = self.mainData.loc[(self.mainData['UF'] == self._initials)]
    df.groupby('Município').sum()
    return df.loc[(df['Dose 2'] == df['Dose 2'].max())]['Município'].to_string(index = False)

  def countyWithLessDose2(self):
    dfOnlyOneState = self.mainData.loc[(self.mainData['UF'] == self.initials)]
    dfByCounty = dfOnlyOneState.groupby('Município').sum().reset_index()
    result = dfByCounty.loc[(dfByCounty['Dose 2'] == dfByCounty['Dose 2'].min())].reset_index()
    return result['Município'].to_string(index = False)
  
  def mostUsedVaccineInState(self):
    dfOnlyOneState = self.mainData.loc[(self.mainData['UF'] == self.initials)]
    dfByVaccine = dfOnlyOneState.groupby('Fabricante').sum()
    result = dfByVaccine.loc[dfByVaccine['Doses Aplicadas'] == dfByVaccine['Doses Aplicadas'].max()].reset_index()
    return result['Fabricante'].to_string(index = False)
    
  def mediaSecondShotByState(self):
    dfAllStates = self.mainData.groupby('UF').mean().reset_index()
    return dfAllStates[['UF','Dose 2']]

  def numberOfVaccinatedEachCapital(self):
    dfOnlyCapitals = self.mainData.groupby(['Cód. IBGE','Município','UF']).sum().reset_index()
    result = dfOnlyCapitals.loc[dfOnlyCapitals['Cód. IBGE'].isin(self.IBGEcodes)]
    return result[['Município', 'Dose 1', 'Dose 2']].reset_index()

  def usedVaccinesInCountry(self):
    dfByVaccine = self.mainData.groupby('Fabricante').sum().reset_index()
    return dfByVaccine

  def mediaAllShotsByCounty(self):
    dfOnlyOneState = self.mainData.loc[(self.mainData['UF'] == self.initials)]
    dfByCounty = dfOnlyOneState.groupby('Município').mean().reset_index()
    return dfByCounty
  
  def averageOfOneState(self):
    dfAllStates = self.mainData.groupby('UF').mean().reset_index()
    return dfAllStates.loc[(dfAllStates['UF'] == self.initials)].reset_index()

  def groupByRegion(self):
    dfByRegion = self.mainData.groupby('Região').sum().reset_index()
    return dfByRegion

class Graphics:

  def __init__(self, datas):
    self.datas = datas

  def mediaSecondShotByStateGraph(self):
    x = self.datas['UF']
    y = self.datas['Dose 2']
    plt.figure(figsize=(10,5))
    plt.title("Media of second shot in each state of Brazil")
    plt.xlabel("States")
    plt.ylabel("Average")
    plt.bar(x, y)
    plt.show()
    

  def numberOfVaccinatedEachCapitalGraph(self):
    w = 0.4
    x = self.datas['Município']
    y1 = self.datas['Dose 1']
    y2 = self.datas['Dose 2']
    plt.figure(figsize=(100,10))
    plt.title("Number of vaccinated in each capital of Brazil")
    plt.xlabel("Capital")
    plt.ylabel("Number")
    bar1 = np.arange(len(x))
    bar2 = [i+w for i in bar1]
    plt.bar(bar1, y1, w, label="Dose one")
    plt.bar(bar2, y2, w, label="Dose two")
    plt.xticks(bar1+w/2, x)
    plt.legend()
    plt.show()

  def usedVaccinesInCountryGraph(self):
    x = self.datas['Fabricante']
    y = self.datas['Doses Aplicadas']
    plt.figure(figsize=(10,5))
    plt.title("Most used vaccine in Brazil")
    plt.xlabel("Producer")
    plt.ylabel("Total Shots")
    colorsBar = ['red', 'yellow', 'green', 'blue']

    for i in range(len(x)):
      producerName = x[i]
      plt.bar(x[i], y[i], label = producerName, color = colorsBar[i])

    plt.legend()
    plt.show()
  
  def mediaShotByStateGraph(self, averageOfState):
    w = 0.4
    x = self.datas['Município']
    y1 = self.datas['Doses Aplicadas']
    y2 = averageOfState
    plt.figure(figsize=(300,10))
    plt.title("Comparasion of average of the state in each county")
    plt.xlabel("County")
    plt.ylabel("Number")
    bar1 = np.arange(len(x))
    bar2 = [i+w for i in bar1]
    plt.bar(bar1, y1, w, label="Average of County")
    plt.bar(bar2, y2, w, label="Average of State")
    plt.xticks(bar1+w/2, x)
    plt.legend()
    plt.show()

  def groupByRegionGraph(self):
    w = 0.2
    x = self.datas['Região']
    y1 = self.datas['Doses Aplicadas']
    y2 = self.datas['Dose 1']
    y3 = self.datas['Dose 2']
    plt.figure(figsize=(20,5))
    plt.title("Comparasion by region")
    plt.xlabel("Region")
    plt.ylabel("Numbers")
    bar1 = np.arange(len(x))
    bar2 = [i+w for i in bar1]
    bar3 = [i+w for i in bar2]
    plt.bar(bar1, y1, w, label="Doses Applies")
    plt.bar(bar2, y2, w, label="Dose one")
    plt.bar(bar3, y3, w, label="Dose two")
    plt.xticks(bar1+w, x)
    plt.legend()
    plt.show()

# Answer question 2(A - B)
statistics = Statistics('TO', dataReturn)
print(f"The total of first dose is {statistics.totalFirstShot()} and the total of second dose is {statistics.totalSecondShot()}")

# Answer question 2(C)
print(f"Total shotes in {statistics.initials} is equal to {statistics.totalShotesInOneState()}")
print(f"The county with most dose 2 is {statistics.countyWithMostDose2()}")
print(f"The county with less dose 2 is {statistics.countyWithLessDose2()}")
print(f"The most used vaccine in {statistics.initials} is {statistics.mostUsedVaccineInState()}")

# Answer question 2(D and graphic)
print('Average of second shot on each state')
print(statistics.mediaSecondShotByState())
graph = Graphics(statistics.mediaSecondShotByState())
graph.mediaSecondShotByStateGraph()

# Answer question 2(E and graphic)
print('Number of vaccinated with dose 1 and dose 2')
print(statistics.numberOfVaccinatedEachCapital())
graph2 = Graphics(statistics.numberOfVaccinatedEachCapital())
graph2.numberOfVaccinatedEachCapitalGraph()

# Addtional data
myData2 = statistics.mediaAllShotsByCounty()
averageOfState = statistics.averageOfOneState()

graph2 = Graphics(myData2)
graph2.mediaShotByStateGraph(averageOfState['Doses Aplicadas'])

myData = statistics.usedVaccinesInCountry()
print(myData)

graph2 = Graphics(myData)
graph2.usedVaccinesInCountryGraph()

myData = statistics.groupByRegion()
print(myData)

graph2 = Graphics(myData)
graph2.groupByRegionGraph()