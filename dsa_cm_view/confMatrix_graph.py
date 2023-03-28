import numpy as np


def confusion_matrix(labelsTrue, labelsOutput, classCount):
    combined = np.asarray([labelsTrue, labelsOutput]).T
    uniqueVals, uniqueCounts = np.unique(combined, return_counts=True, axis=0)
    confusionMatrix = np.zeros((classCount, classCount))
    allUnique = np.sort(np.unique(combined.astype(int)))

    mapped = {uniqueVal: val for uniqueVal, val in zip(
        allUnique.tolist(), range(allUnique.size))}

    for (val, count) in zip(uniqueVals, uniqueCounts):
        confusionMatrix[mapped[int(val[0])], mapped[int(val[1])]] += count
    return confusionMatrix



# import pandas as pd

# confusionMatrix = confusion_matrix(labels, outputLabels, classCount=ip.classCount)
# df = pd.DataFrame(confusionMatrix)

# names = {ind: name for ind, name in zip(df.index, ip.uniqueClasses)}

# df.rename(columns=names, index=names, inplace=True)
# df.astype(int).style.background_gradient(cmap ='viridis').set_properties(**{'font-size': '20px'})