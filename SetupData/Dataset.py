# Wraps around a dataframe object to provide randomized training, testing, validation data to a NN
from typing import Tuple

import numpy as np
import torch
import pandas as pd
import definitions


class DatasetFromDataframe(torch.utils.data.Dataset):
    def __init__(self, inputDataframe : pd.DataFrame, outputDataframe : pd.DataFrame):
        self.x = self.convertDataframeToDataset(inputDataframe)
        self.y = self.convertDataframeToDataset(outputDataframe)
        self.xHeaders = inputDataframe.columns
        self.yHeaders = outputDataframe.columns

    def convertDataframeToDataset(self, dataFrame : pd.DataFrame) -> np.ndarray:
        return dataFrame.to_numpy(dtype='float32')

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return [self.x[idx], self.y[idx]]

    def get_splits(self, n_val=0.1, n_test=0.1):
        # Determine sizes
        test_size = round(n_test * len(self.x))
        val_size = round(n_val * len(self.x))
        train_size = len(self.x) - test_size - val_size
        # Calculate the split
        return torch.utils.data.random_split(self, [train_size, val_size, test_size])

    def getInputDimensions(self):
        return len(self.x[0,:])

    def getOutputDimensions(self):
        return len(self.y[0,:])

class DatasetFromCsv(DatasetFromDataframe):
    def __init__(self, dataName):
        inputPath = definitions.createPathToCsvDataFile(dataName, isInputs=True)
        outputPath = definitions.createPathToCsvDataFile(dataName, isInputs=False)
        xDataFrame = pd.read_csv(inputPath)
        yDataFrame = pd.read_csv(outputPath)
        super().__init__(xDataFrame, yDataFrame)
