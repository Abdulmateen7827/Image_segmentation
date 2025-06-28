import os
import sys
from src.logger import logging
from src.exception import CustomException
import tensorflow as tf

import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.components.data_preprocessing import DataPreprocessing
from src.pipeline.training_pipeline import ModelTrainer
from src.pipeline.prediction_pipeline import PredictPipeline


path = 'data' 

@dataclass
class DataIngestionConfig:

    images_data: str = os.path.join(path, 'images')
    masks_data: str = os.path.join(path, 'masks')

@dataclass
class DimensionsConfig:
    EPOCHS = 50
    VAL_SUBSPLITS = 5
    BUFFER_SIZE = 500
    BATCH_SIZE = 32

dim_cofig = DimensionsConfig()
logging.info('Returned images and masks in lists')
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            image_list_ = os.listdir(self.data_ingestion_config.images_data)
            mask_list_ = os.listdir(self.data_ingestion_config.masks_data)

            image_list = [self.data_ingestion_config.images_data+"/"+i for i in image_list_]
            mask_list = [self.data_ingestion_config.masks_data+"/"+i for i in mask_list_]
            

            image_filenames = tf.constant(image_list)
            mask_filenames = tf.constant(mask_list)

            dataset = tf.data.Dataset.from_tensor_slices((image_filenames, mask_filenames))
            logging.info("Data ingestion is completed")

            return dataset



            
            

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    
    obj = DataIngestion()
    dataset = obj.initiate_data_ingestion()

    preprocessor = DataPreprocessing()
    dataset = dataset.map(preprocessor.initializing_preprocessing)
    logging.info("preprocessing completed")

    dataset.batch(dim_cofig.BATCH_SIZE)

    train_dataset = dataset.cache().shuffle(dim_cofig.BUFFER_SIZE).batch(dim_cofig.BATCH_SIZE)

    train = ModelTrainer()
    logging.info("training started")
    train.initialize_training(train_dataset=train_dataset,epoch=dim_cofig.EPOCHS)








    


