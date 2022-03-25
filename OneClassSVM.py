from sklearn.svm import OneClassSVM
import csv
import os

# import numpy as np
# #import matplotlib.pyplot as plt
# #import matplotlib.font_manager

# ArrayOfTrainingData = [[-1000],[24],[25],[26],[27],[28],[29],[30],[1000]]

ArrayOfTrainingData = []

ArrayOfTestData = [[24],[25],[26],[27],[28]]

ArrayOfOutlierData = [[100],[-1],[26],[-30],[24],[28]]

def GetDataFromCSV():
    with open('readings.csv', 'r') as CSVData:
        Reader = csv.reader(CSVData)
        for row in Reader:
            row[0] = int(row[0])
#             print(row[0])
            ArrayOfTrainingData.append(row)
            
            
if __name__ == "__main__":
    GetDataFromCSV()
    
    clf = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1).fit(ArrayOfTrainingData)
    
    TrainingPrediction = clf.predict(ArrayOfTrainingData)
    TestPrediction = clf.predict(ArrayOfTestData)
    TestScores = clf.score_samples(ArrayOfTestData)
    OutlierPrediction = clf.predict(ArrayOfOutlierData)
    
#     print(TrainingPrediction)
#     for i in TrainingPrediction:
#         print(i)
        
    print(TestPrediction)
    print(OutlierPrediction)
    print(TestScores)
    
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