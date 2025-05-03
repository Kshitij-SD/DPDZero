from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_merging import DataMerging
from mlProject import logger

STAGE_NAME = "Data Merging stage"

class DataMergingTrainingPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        data_merging_config = config.get_data_merging_config()
        data_merging = DataMerging(config=data_merging_config)
        data_merging.merge_data()