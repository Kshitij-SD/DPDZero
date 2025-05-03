import os
import urllib.request as request
import zipfile
from mlProject import logger
from mlProject.utils.common import get_size
import pandas as pd
from mlProject.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def copy_data(self):

            agents_roster = pd.read_csv(self.config.data_dir + "/agent_roster.csv")
            call_logs = pd.read_csv(self.config.data_dir + "/call_logs.csv")
            disposition_summary = pd.read_csv(self.config.data_dir + "/disposition_summary.csv")
            
            agents_roster.to_csv(self.config.root_dir + "/agent_roster.csv" ,index=False)
            call_logs.to_csv(self.config.root_dir + "/call_logs.csv" ,index=False)
            disposition_summary.to_csv(self.config.root_dir + "/disposition_summary.csv" ,index=False)
            
            logger.info("Data Copied to Artifacts")
            