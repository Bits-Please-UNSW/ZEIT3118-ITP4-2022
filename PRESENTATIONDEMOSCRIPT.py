import csv 
from datetime import datetime, timedelta
import threading

#Telemetry Collector imports
import time
import board
import adafruit_dht
import psutil
from datetime import datetime
import csv


#OneClassSVM imports
from multiprocessing.sharedctypes import Value
from sklearn.svm import OneClassSVM
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
import csv
import os

# import numpy as np
# #import matplotlib.pyplot as plt
# #import matplotlib.font_manager

# ArrayOfTrainingData = [[-1000],[24],[25],[26],[27],[28],[29],[30],[1000]]


ArrayOfTrainingData = []

# ArrayOfTestData = [[24],[25],[26],[27],[28]]

# ArrayOfOutlierData = [[100],[-1],[26],[-30],[24],[28]]


def GetDataFromCSV():
    CurrentTime = datetime.now().replace(microsecond=0)
    # print(CurrentTime)
    GetFromTime = CurrentTime - timedelta(days = 1)
    # print(GetFromTime)

    with open('./TESTreadings.csv', 'r') as CSVData:
        Reader = csv.reader(CSVData)
        for row in Reader:
            # row[0] = int(row[0])
            row[0] = str(row[0])
            row[1] = int(row[1])
            row[2] = int(row[2])
            # print(row[0])
            # print(row[1])
            # print(row[2])
            DataTimeStamp = (datetime.fromisoformat(row[0]))
            if (DataTimeStamp >= GetFromTime):
                NewRow = []
                NewRow.append(int(row[1]))
                NewRow.append(int(row[2]))
                # print(row)
                ArrayOfTrainingData.append(NewRow)


def PrintOutcomes(InputDataSet, OutputDataSet):
    ArrayOfMappedOutcomes = []
    if (len(InputDataSet) == len(InputDataSet)):
        Count = 0
        for i in InputDataSet:
            InputValue0 = int(InputDataSet[Count][0])
            InputValue1 = int(InputDataSet[Count][1])
            OutputValue = int(OutputDataSet[Count])
            if (OutputValue == -1):
                Prediction = "Abnormal"
            elif (OutputValue == 1):
                Prediction = "Normal"
            StringToAppend = ("Value: {},{} is {} (SVMOutput: {})".format(InputValue0,InputValue1,Prediction,OutputValue))
            # print(StringToAppend)
            ArrayOfMappedOutcomes.append(StringToAppend)
            Count = Count + 1
        return ArrayOfMappedOutcomes


def GetPlotBoundaries(InputDataSet):
    MinTemp, MaxTemp, MinHumid, MaxHumid = 101, -100, 101, -100
    for Entries in InputDataSet:
        if (Entries[0] < MinTemp):
            MinTemp = Entries[0]
        if (Entries[0] > MaxTemp):
            MaxTemp = Entries[0]
        if (Entries[1] < MinHumid):
            MinHumid = Entries[1]
        if (Entries[1] > MaxHumid):
            MaxHumid = Entries[1]

    ValueToAdjustBy = 5
    ArrayofBoundaries = [MinTemp-ValueToAdjustBy, MaxTemp+ValueToAdjustBy, 
                        MinHumid-ValueToAdjustBy, MaxHumid+ValueToAdjustBy]

    print(f"Plot boundaries calculated at: {ArrayofBoundaries}")
    return ArrayofBoundaries



def PerformAnalysis():
    GetDataFromCSV()
    print('----------STATUS: DONE GETTING DATA FROM CSV!----------')

    # print(ArrayOfTrainingData)
    ArrayOfTrainingData_NumpyArrayFormat = np.array(ArrayOfTrainingData)
    # print(ArrayOfTrainingData_NumpyArrayFormat)

    # ArrayOfTrainingData.append([30]) #test if outlier in training set is detected as such
    
    clf = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.fit(ArrayOfTrainingData_NumpyArrayFormat)
    
    TrainingPrediction = clf.predict(ArrayOfTrainingData_NumpyArrayFormat)
    # TestPrediction = clf.predict(ArrayOfTestData)
    # TestScores = clf.score_samples(ArrayOfTestData)
    # OutlierPrediction = clf.predict(ArrayOfOutlierData)
    
    # print(TrainingPrediction)
    # for i in TrainingPrediction:
    #     print(i)

    #PrintOutcomes(ArrayOfTrainingData, TrainingPrediction)
    # print(TestPrediction)
    # print(OutlierPrediction)
    # print(TestScores)
    
#     n_error_train = TrainingPrediction[TrainingPrediction == -1].size
#     n_error_test = TestPrediction[TestPrediction == -1].size
#     n_error_outliers = OutlierPrediction[OutlierPrediction == 1].size
#     print(n_error_train)
#     print(n_error_test)
#     print(n_error_outliers)
    
#     i = 0
#     while i < 10400:
#         if TestPrediction[i] == -1:
#             print(ArrayOfTestData[i])
#         i = i + 1

    
        
#    ScoredSamples = clf.score_samples(ArrayOfData)
#    for i in ScoredSamples:
#        print(i)

    ####PLOT FUNCTIONS####

    xx, yy = np.meshgrid(np.linspace(0, 100, num=100), np.linspace(0, 100, num=100))
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    # print(Z) #Debug
    Z = Z.reshape(xx.shape)
    # print(Z) # Debug

    plt.title("Data Anomaly Detection Plot")
    plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
    a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors="darkred")
    plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors="palevioletred")

    s = 20
    b1 = plt.scatter(ArrayOfTrainingData_NumpyArrayFormat[:, 0], ArrayOfTrainingData_NumpyArrayFormat[:, 1], c="white", s=s, edgecolors="k")
    # b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c="blueviolet", s=s, edgecolors="k")
    # c = plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c="gold", s=s, edgecolors="k")
    plt.axis("tight")

    # plt.axis([0, 100, 0, 100])
    Boundaries = GetPlotBoundaries(ArrayOfTrainingData)
    plt.axis([Boundaries[0], Boundaries[1], Boundaries[2], Boundaries[3]])

    plt.xlabel('Temperature (*C)')
    plt.ylabel('Humidity (%)')
    # plt.xlim((0, 30))
    # plt.ylim((0, 30))
    plt.legend(
        [a.collections[0], b1],
        [
            "learned frontier",
            "training observations",
            "new regular observations",
            "new abnormal observations",
        ],
        loc="upper left",
        prop=matplotlib.font_manager.FontProperties(size=11),
    )

    CurrentTime = datetime.now().replace(second=0, microsecond=0)
    plt.savefig(fname='/var/www/html/pages/Test') #Save most recent result to webserver
    plt.savefig(fname=(f'/var/www/html/images/data_graph_archive/{CurrentTime}')) #Save copy of most recent result to archive with stamp
    plt.savefig(fname='Test') #Save most recent result here as debug
    plt.show()



##### Telemetry Collection METHODS #####
# Method to write sensor data to CSV file
def AppendToCSV(DataToWrite):
    with open('./TESTreadings.csv', 'a') as csvfile:
        CSVWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        CSVWriter.writerow(DataToWrite)
        print("Appended new row to CSV File: {} from data >> Time: {}, Temperature: {}*C,  Humidity: {}%".format(DataToWrite, DataToWrite[0], DataToWrite[1],  DataToWrite[2]))
        


def CollectTelemetry():
    # First check if libgpiod process is running. If so terminate running instance.
    for process in psutil.process_iter():
        if (process.name() == 'libgpiod_pulsein' or process.name() == 'libgpiod_pulsei'):
            process.kill()

    DHT11Sensor = adafruit_dht.DHT11(4)
    while True:
        try:
            Timestamp = datetime.now().replace(microsecond=0)
            Temperature = DHT11Sensor.temperature
            Humidity = DHT11Sensor.humidity
            TimestampTempHumidArray = [Timestamp, Temperature, Humidity]
            # print("{} > Temperature: {}*C,  Humidity: {}% ".format(Timestamp, Temperature, Humidity)) #Uncomment for debug
            AppendToCSV(TimestampTempHumidArray)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            DHT11Sensor.exit()
            raise error
        
        # Sleep for two seconds before taking next measurement
        time.sleep(2.0)



##### MAIN METHOD #####
if __name__ == "__main__":

    AnomalousDataSmple1 = [(datetime(2022, 5, 10, 22, 11, 2)), int(100), int(100)]
    AppendToCSV(AnomalousDataSmple1)
    AnomalousDataSmple1 = [(datetime(2022, 5, 10, 22, 11, 2)), int(105), int(105)]
    AppendToCSV(AnomalousDataSmple1)
    AnomalousDataSmple1 = [(datetime(2022, 5, 10, 22, 11, 2)), int(-50), int(-50)]
    AppendToCSV(AnomalousDataSmple1)

    print("----------PERFORMING ANALYSIS----------")
    PerformAnalysis()
