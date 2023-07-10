import csv
from sklearn.svm import SVC

def get_model(trainset):
    csvFile = open(trainset, 'r')
    reader = csv.reader(csvFile)
    classification = []
    data = []
    for row in reader:
        if row[0] == 'Class': continue
        classification.append(str(row[0]))
        data.append([float(x) if x != 0 else 0 for x in row[1:]])

    model = SVC()

    model.fit(data, classification)

    return model