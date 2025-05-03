from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    data_dir: Path
    
@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_dir: Path
    STATUS_FILE: str
    all_schema: dict
    
@dataclass(frozen=True)
class DataMergingConfig:
    root_dir: Path
    data_dir: Path
    merged_data_dir: Path
    
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataFeatureConfig:
    root_dir: Path
    data_dir: Path
    output_dir: Path