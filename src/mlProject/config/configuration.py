from mlProject.constants import *
from mlProject.utils.common import read_yaml,create_directories
from mlProject.entity.config_entity import DataIngestionConfig, DataValidationConfig
from mlProject.entity.config_entity import DataMergingConfig
from mlProject.entity.config_entity import DataFeatureConfig

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            data_dir = config.data_dir,
        )
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            data_dir = config.data_dir,
            STATUS_FILE=config.STATUS_FILE,
            all_schema=schema,
        )

        return data_validation_config
    
    def get_data_merging_config(self) -> DataMergingConfig:
        config = self.config.data_merging

        create_directories([config.root_dir])

        data_merging_config = DataMergingConfig(
            root_dir = config.root_dir,
            data_dir = config.data_dir,
            merged_data_dir = config.merged_data_dir
        )
        return data_merging_config
    def get_feature_config(self) -> DataFeatureConfig:
        config = self.config.feature_engineering

        create_directories([config.root_dir])

        data_feature_config = DataFeatureConfig(
            root_dir = config.root_dir,
            data_dir = config.data_dir,
            output_dir = config.output_dir
        )
        return data_feature_config