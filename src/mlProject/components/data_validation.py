import os
from mlProject import logger
import re
import pandas as pd
from datetime import datetime
from mlProject.entity.config_entity import DataValidationConfig

class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = True
            error_messages = []
            data = pd.read_csv(self.config.data_dir, dtype={'call_date': str})
            all_cols = list(data.columns)
            expected_cols = list(self.config.all_schema.keys())

            missing_cols = [col for col in expected_cols if col not in all_cols]
            if missing_cols:
                validation_status = False
                error_messages.append(f"Missing columns: {missing_cols}")

            if 'org_id' in data.columns:
                if not data['org_id'].isin(['O1', 'O2', 'O3']).all():
                    validation_status = False
                    invalid_ord_ids = data[~data['org_id'].isin(['O1', 'O2', 'O3'])]['org_id'].unique().tolist()
                    error_messages.append(f"Invalid ord_id values found: {invalid_ord_ids}")
            else:
                error_messages.append("Column 'org_id' not found.")

            if 'agent_id' in data.columns:
                valid_agents = [f"A{str(i).zfill(3)}" for i in range(1, 21)]
                if not data['agent_id'].isin(valid_agents).all():
                    validation_status = False
                    invalid_agents = data[~data['agent_id'].isin(valid_agents)]['agent_id'].unique().tolist()
                    error_messages.append(f"Invalid agent_id values found: {invalid_agents}")
            else:
                error_messages.append("Column 'agent_id' not found.")

            if 'call_date' in data.columns:
                data['call_date'] = pd.to_datetime(data['call_date'], errors='coerce')
                data['call_date'] = data['call_date'].dt.strftime('%#m/%#d/%Y')
                invalid_dates = []
                date_pattern = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$") 

                for date_str in data['call_date']:
                    if not isinstance(date_str, str) or not date_pattern.fullmatch(date_str.strip()):
                        invalid_dates.append(str(date_str))

                if invalid_dates:
                    validation_status = False
                    error_messages.append(f"Invalid call_date formats (expected M/D/YYYY): {invalid_dates}")
            else:
                error_messages.append("Column 'call_date' not found.")

            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}\n")
                if error_messages:
                    for msg in error_messages:
                        f.write(f"{msg}\n")

            return validation_status

        except Exception as e:
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation failed due to unexpected error: {str(e)}\n")
            raise e