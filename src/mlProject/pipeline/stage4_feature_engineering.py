from mlProject.config.configuration import ConfigurationManager
from mlProject.components.feature_engineering import FeatureEngineering
from mlProject import logger

STAGE_NAME = "Feature Engineering stage"

class FeatureEngineeringTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_feature_config = config.get_feature_config()
        data_feature = FeatureEngineering(config=data_feature_config)
        data_feature.transform()