# This code imports the required modules and classes
import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Importing custome modules
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

# This class contains the configuration information for data ingestion
@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts',"train.csv")
    test_data_path:str = os.path.join('artifacts',"test.csv")
    raw_data_path:str = os.path.join('artifacts',"data.csv")

# This class defines the data ingestion component
class DataIngestion:
    def __init__(self):
        # This line creates an instance of the DataIngestionConfig class and assigns it to a variable
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        # This line logs a message indicating that the data ingestion process has started
        logging.info("Entered the data ingestion method or component")
        try:
            # This line reads the CSV file located at the specified path into a Pandas DataFrame
            df = pd.read_csv('notebook\data\stud.csv')
            # This line logs a message indicating that the DataFrame was successfully read
            logging.info('Read the dataset as dataframe')

            # This line creates the directory specified in the train_data_path attribute, if it does not exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            # This line writes the entire DataFrame to a CSV file at the specified path
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # This line logs a message indicating that the train/test split process has started
            logging.info("Train test Split initiated")

            # This line splits the DataFrame into a train set and a test set, with a test size of 0.2 and a random state of 42
            train_set, test_set = train_test_split(df,test_size=0.2,random_state=42)

            # This line writes the train set DataFrame to a CSV file at the specified path
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            # This line writes the test set DataFrame to a CSV file at the specified path
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            # This line logs a message indicating that the data ingestion
            logging.info("Ingestion of the data is completed")

            # This line returns a tuple containing the file paths for the train and test datasets.
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        
        # This line initiates an exception handler for any exception that occurs in the try block.
        except Exception as e:
            # This line raises a CustomException with the exception object e and the sys module details. 
            # This is done to provide the caller with a detailed error message that includes the error type, error message, 
            # and the file and line number where the error occurred.
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))