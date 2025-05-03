import pandas as pd
import os
import urllib.request as request
import zipfile
from mlProject import logger
from mlProject.utils.common import get_size
from mlProject.entity.config_entity import DataMergingConfig

class DataMerging:
    def __init__(self, config: DataMergingConfig):
        self.config = config

    def merge_data(self):
        call_logs = pd.read_csv(self.config.data_dir + '/call_logs.csv')
        agent_roster = pd.read_csv(self.config.data_dir + '/agent_roster.csv')
        disposition_summary = pd.read_csv(self.config.data_dir + '/disposition_summary.csv')

        call_logs['call_date'] = pd.to_datetime(call_logs['call_date'])
        disposition_summary['call_date'] = pd.to_datetime(disposition_summary['call_date'])

        agent_login = pd.merge(
            agent_roster,
            disposition_summary,
            on=['agent_id', 'org_id'],
            how='left'
        )

        merged_df = pd.merge(
            agent_login,
            call_logs,
            on=['agent_id', 'org_id', 'call_date'],
            how='left'
        )
        merged_df.to_csv(self.config.merged_data_dir, index=False)
        
        logger.info(f"Data merged and saved to {self.config.merged_data_dir}")
        