#####General imports#####
import csv 
from datetime import datetime, timedelta
import threading
import time
import mysql.connector

#####Telemetry Collector imports#####
import adafruit_dht
import psutil

#####OneClassSVM imports#####
from sklearn.svm import OneClassSVM
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager



#####Global vairables#####

ArrayOfOriginalTrainingData = []
ArrayOfTrainingData = []



#####METHODS#####

def GetDataFromSQL():
    '''Method that fetches and processes all raw data stored in the SQL server'''
    ArrayOfOriginalTrainingData.clear()
    ArrayOfTrainingData.clear()

    CurrentTime = datetime.now().replace(microsecond=0)

    GetFromTime = CurrentTime - timedelta(days = 1)

    SQLConnectionAnalysis = mysql.connector.connect(user='dartuser', password='password1', 
                                                    host='localhost', database='dart_data')

    SQLCursor = SQLConnectionAnalysis.cursor()

    PreparedQuery = str(f"SELECT * FROM sensor_data WHERE DATETIMESTAMP >= ('{str(GetFromTime)}');")
    SQLCursor.execute(PreparedQuery)

    for row in SQLCursor:
        ConvertedRow = []
        ConvertedRow.append(str(row[0]))
        ConvertedRow.append(int(row[1]))
        ConvertedRow.append(int(row[2]))

        DataTimeStamp = (datetime.fromisoformat(ConvertedRow[0]))
        # print(ConvertedRow) #uncomment for debug

        NewRow = []
        NewRow.append(int(ConvertedRow[1]))
        NewRow.append(int(ConvertedRow[2]))

        RawRow = []
        RawRow.append(str(ConvertedRow[0]))
        RawRow.append(int(ConvertedRow[1]))
        RawRow.append(int(ConvertedRow[2]))

        ArrayOfTrainingData.append(NewRow)
        ArrayOfOriginalTrainingData.append(RawRow)

    SQLCursor.close()
    SQLConnectionAnalysis.close()

    print("Sorted Array Lengths are: ")     #PRINT FOR DEBUG
    print(len(ArrayOfOriginalTrainingData)) #PRINT FOR EBUG
    print(len(ArrayOfTrainingData))         #PRINT FOR DEBUG


def StoreOutcomes(InputDataSet, OutputDataSet):
    '''Method used to store/export all abnormal data entries to CSV file format (used to display processed data on webpage'''
    #Clear webapps logged anomalies file contents
    file = open('/var/www/html/data/Anomalies.csv',"r+")
    file.truncate(0)
    file.close()

    file = open('/var/www/html/data/RecentAnomalies.csv',"r+")
    file.truncate(0)
    file.close()

    #Add new contents
    ArrayOfMappedOutcomes = []
    if (len(InputDataSet) == len(InputDataSet)):
        CurrentTime = datetime.now().replace(microsecond=0)

        ReversedInputDataSet = InputDataSet[::-1]
        ReversedOutputDataSet = OutputDataSet[::-1]
        Count = 0
        for i in reversed(InputDataSet):
            # print(i)  # uncomment for debug
            InputValue0 = str(ReversedInputDataSet[Count][0])
            InputValue1 = int(ReversedInputDataSet[Count][1])
            InputValue2 = int(ReversedInputDataSet[Count][2])
            OutputValue = int(ReversedOutputDataSet[Count])

            DataTimeStamp = (datetime.fromisoformat(InputValue0))
            GetFromTime = CurrentTime - timedelta(days = 1)
            GetFromTimeRecent = CurrentTime - timedelta(minutes = 30)

            #Get anomalies in last 24 hours, append them to webpage's Anomalies.csv data feed
            if (DataTimeStamp >= GetFromTime):
                if (OutputValue == -1):
                    Prediction = "Abnormal"
                    StringToAppend = ("{}, {}*C, {}%".format(InputValue0,InputValue1,InputValue2))
                    with open('/var/www/html/data/Anomalies.csv', 'a') as anomaliescsvfile:
                        AnomaliesCSVWriter = csv.writer(anomaliescsvfile, delimiter='.', quoting=csv.QUOTE_NONE)
                        AnomaliesCSVWriter.writerow([StringToAppend])
                elif (OutputValue == 1):
                    Prediction = "Normal"

            #Get anomalies in last 30 minutes, append them to webpage's RecentAnomalies.csv data feed
            if (DataTimeStamp >= GetFromTimeRecent):
                if (OutputValue == -1):
                    Prediction = "Abnormal"
                    StringToAppend = ("{}, {}*C, {}%".format(InputValue0,InputValue1,InputValue2))
                    with open('/var/www/html/data/RecentAnomalies.csv', 'a') as anomaliescsvfile2:
                        AnomaliesCSVWriter2 = csv.writer(anomaliescsvfile2, delimiter='.', quoting=csv.QUOTE_NONE)
                        AnomaliesCSVWriter2.writerow([StringToAppend])
                elif (OutputValue == 1):
                    Prediction = "Normal"

            Count = Count + 1

        return ArrayOfMappedOutcomes


def GetPlotBoundaries(InputDataSet):
    '''Method to calculate plot boundaries, used for creating graphs of SVM Output'''
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
    '''Method used to perform One Class SVM Machine Learning Algorithm analysis of data, and plot the outcome to a matplotlib graph'''
    GetDataFromSQL()
    print('----------STATUS: DONE GETTING DATA FROM SQL!----------')

    ArrayOfTrainingData_NumpyArrayFormat = np.array(ArrayOfTrainingData)
    
    clf = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.fit(ArrayOfTrainingData_NumpyArrayFormat)
    
    TrainingPrediction = clf.predict(ArrayOfTrainingData_NumpyArrayFormat)

    StoreOutcomes(ArrayOfOriginalTrainingData, TrainingPrediction)
    print('OUTCOMES SUCCESSFULLY STORED!')
    # print(TestPrediction) #Uncomment for debug
    # print(OutlierPrediction) #Uncomment for debug
    # print(TestScores) #Uncomment for debug

    ####PLOT FUNCTIONS####
    xx, yy = np.meshgrid(np.linspace(0, 100, num=100), np.linspace(0, 100, num=100))
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    # print(Z) ##Uncomment for debug
    Z = Z.reshape(xx.shape)
    # print(Z) # #Uncomment for debug

    plt.title("Anomaly Detection")
    plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
    a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors="darkred")
    plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors="palevioletred")

    s = 20
    b1 = plt.scatter(ArrayOfTrainingData_NumpyArrayFormat[:, 0], ArrayOfTrainingData_NumpyArrayFormat[:, 1], c="white", s=s, edgecolors="k")
    plt.axis("tight")

    Boundaries = GetPlotBoundaries(ArrayOfTrainingData)
    plt.axis([Boundaries[0], Boundaries[1], Boundaries[2], Boundaries[3]])

    plt.xlabel('Temperature (*C)')
    plt.ylabel('Humidity (%)')

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
    plt.savefig(fname='/var/www/html/pages/CurrentDataGraph') #Save most recent result to webserver
    plt.savefig(fname=(f'/var/www/html/images/data_graph_archive/{CurrentTime}')) #Save copy of most recent result to archive with stamp
    plt.savefig(fname='CurrentLatestGraph') #Save most recent result here as debug
    # plt.show() #Uncomment for debug

    plt.close('all') #Close figures to prevent new ones failing


##### Telemetry Collection METHODS #####
def AppendToSQL(SQLConnection, DataToWrite):
    '''Method to append given DataToWrite Paramater to SQL database. Used for logging raw telemetry data'''
    SQLCursor = SQLConnection.cursor()
    PreparedStatement = str(f"INSERT INTO sensor_data VALUES ('{str(DataToWrite[0])}', {DataToWrite[1]}, {DataToWrite[2]});")
    SQLCursor.execute(PreparedStatement)
    SQLConnection.commit()
    SQLCursor.close()
    print("Appended new row to SQL: {} from data >> Time: {}, Temperature: {}*C,  Humidity: {}%".format(DataToWrite, DataToWrite[0], DataToWrite[1],  DataToWrite[2]))
        

def CollectTelemetry(SQLConnection):
    '''Method used to collect data from sensors via the relevant packages (libgpio, board, adafruit)'''
    # First check if libgpiod process is running. If so terminate running instance.
    for process in psutil.process_iter():
        if (process.name() == 'libgpiod_pulsein' or process.name() == 'libgpiod_pulsei'):
            process.kill()

    DHT11Sensor = adafruit_dht.DHT11(4)
    while True:
        try:
            Timestamp = str(datetime.now().replace(microsecond=0))
            Temperature = int(DHT11Sensor.temperature)
            Humidity = int(DHT11Sensor.humidity)
            TimestampTempHumidArray = [Timestamp, Temperature, Humidity]
            # print("{} > Temperature: {}*C,  Humidity: {}% ".format(Timestamp, Temperature, Humidity)) #Uncomment for debug
            AppendToSQL(SQLConnection, TimestampTempHumidArray)
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
    '''Method used to coordinate the Telemetry Collection and Machine Learning Data Analysis processes/threads'''

    SQLConnectionTelemetry = mysql.connector.connect(user='dartuser', password='password1', 
                                            host='localhost', database='dart_data')

    TelemetryCollectionThread = threading.Thread(target=CollectTelemetry, args=(SQLConnectionTelemetry,))
    TelemetryCollectionThread.start()

    print("STARTED")
    PerformAnalysis()
    while True:
        time.sleep(1800)
        print("----------PERFORMING ANALYSIS----------")
        PerformAnalysis()