import csv 
from datetime import datetime, timedelta


ArrayOfTrainingData = []

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

GetDataFromCSV()
for i in ArrayOfTrainingData:
    print(i)