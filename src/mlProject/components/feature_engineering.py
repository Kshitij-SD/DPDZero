import pandas as pd
import os
import urllib.request as request
import zipfile
from mlProject import logger
from mlProject.utils.common import get_size
from mlProject.entity.config_entity import DataFeatureConfig

class FeatureEngineering:
    def __init__(self, config: DataFeatureConfig):
        self.config = config

    def transform(self):
        merged_df = pd.read_csv(self.config.data_dir)
        agent_performance = merged_df.groupby(['agent_id', 'users_first_name', 'users_last_name', 
                                        'users_office_location', 'org_id', 'call_date']).apply(self.calculate_metrics).reset_index()
        agent_performance = agent_performance[[
            'agent_id', 'users_first_name', 'users_last_name', 'users_office_location', 'org_id',
            'call_date', 'login_time', 'presence', 'total_calls', 'unique_loans_contacted',
            'connect_rate', 'avg_call_duration'
        ]]
        
        agent_performance['connect_rate'] = agent_performance['connect_rate'].apply(lambda x: f"{x:.2%}")
        agent_performance.to_csv(self.config.output_dir, index=False)
            
    
    def calculate_metrics(self,group):
        total_calls = group['call_id'].nunique()
        unique_loans = group['installment_id'].nunique()
        
        completed_calls = group[group['status'] == 'completed']['call_id'].nunique()
        connect_rate = completed_calls / total_calls if total_calls > 0 else 0
        
        avg_duration = group['duration'].mean() if total_calls > 0 else 0
        presence = 1 if pd.notna(group['login_time'].iloc[0]) else 0
        
        return pd.Series({
            'total_calls': total_calls,
            'unique_loans_contacted': unique_loans,
            'connect_rate': connect_rate,
            'avg_call_duration': avg_duration,
            'presence': presence,
            'login_time': group['login_time'].iloc[0] if pd.notna(group['login_time'].iloc[0]) else 'Not Logged In'
        })