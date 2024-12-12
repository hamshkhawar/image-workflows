import pydantic
from pathlib import Path
from typing import Dict
from typing import Union
import yaml


GITHUB_TAG = "https://raw.githubusercontent.com"


OUT_PATH = Path.cwd()


MANIFEST_URLS = {
            "bbbc_download": f"{GITHUB_TAG}/saketprem/polus-plugins/bbbc_download/utils/bbbc-download-plugin/plugin.json",
            "file_renaming": f"{GITHUB_TAG}/hamshkhawar/image-tools/refs/heads/fix_whitespaces_filerenaming/formats/file-renaming-tool/plugin.json",
            "ome_converter": f"{GITHUB_TAG}/hamshkhawar/image-tools/refs/heads/fix_worker_omeconverter/formats/ome-converter-tool/plugin.json",
            "estimate_flatfield": f"{GITHUB_TAG}/hamshkhawar/image-tools/refs/heads/update_basicpy_dependency/regression/basic-flatfield-estimation-tool/plugin.json",
            "apply_flatfield": f"{GITHUB_TAG}/PolusAI/image-tools/refs/heads/master/transforms/images/apply-flatfield-tool/plugin.json",
            "kaggle_nuclei_segmentation": f"{GITHUB_TAG}/PolusAI/image-tools/refs/heads/master/segmentation/kaggle-nuclei-segmentation-tool/plugin.json",
            "ftl_plugin": f"{GITHUB_TAG}/nishaq503/image-tools/fix/ftl-label/transforms/images/polus-ftl-label-plugin/plugin.json",
            "nyxus_plugin": f"{GITHUB_TAG}/hamshkhawar/image-tools/refs/heads/nyxus_bug/features/nyxus-tool/plugin.json",
            "tabular_feat_concat": f"{GITHUB_TAG}/hamshkhawar/tabular-tools/refs/heads/tabular-concat/transforms/tabular-feature-concat-tool/plugin.json",
            "tabular_threshold":f"{GITHUB_TAG}/hamshkhawar/tabular-tools/refs/heads/tabular-thres/transforms/tabular-thresholding-tool/plugin.json",
            "tabular_statistics":f"{GITHUB_TAG}/hamshkhawar/tabular-tools/refs/heads/tabular_statistic/features/tabular-statistics-tool/plugin.json",
            "montage_url" :f"{GITHUB_TAG}/PolusAI/image-tools/refs/heads/master/transforms/images/montage-tool/plugin.json",
            "image_assembler_url": f"{GITHUB_TAG}/PolusAI/image-tools/refs/heads/master/transforms/images/image-assembler-tool/plugin.json",
            "precompute_slide_url": f"{GITHUB_TAG}/PolusAI/image-tools/refs/heads/master/visualization/precompute-slide-tool/plugin.json"
        }


# Define keys as frozensets for immutability
OPTIONAL_KEYS = frozenset(["map_directory", 
                           "file_extension",
                           "background_correction", 
                            "pixel_per_micron",
                            "neighbor_dist",
                            "neg_control",
                            "pos_control",
                            "thresh_varname",
                            "thresh_type",
                            "false_positive_rate",
                            "num_bins",
                            "n",
                            "statistics"
                            ])

ANALYSIS_KEYS = frozenset([
    "name", "inp_dir", "meta_dir", "file_pattern", "out_file_pattern",  "seg_pattern", 
    "ff_pattern", "df_pattern", "group_by", "map_directory", "features", 
    "file_extension", "background_correction", "container_engine", "pixel_per_micron",
    "neighbor_dist","neg_control","pos_control","thresh_varname","thresh_type","false_positive_rate","num_bins", "n", 
    "statistics"
])


SEG_KEYS = frozenset([
    "name", "inp_dir", "file_pattern", "out_file_pattern",  "seg_pattern", 
    "ff_pattern", "df_pattern", "group_by", "map_directory",
    "background_correction","container_engine"
])


VIZ_KEYS = frozenset([
    "name", "inp_dir", "file_pattern", "out_file_pattern", "seg_pattern", 
    "layout", "pyramid_type", "image_type", "ff_pattern", "df_pattern", "group_by", 
    "map_directory", "background_correction", "container_engine"
])

# Mapping workflows to their respective keys
WORKFLOW_KEYS = {
    "analysis": ANALYSIS_KEYS,
    "segmentation": SEG_KEYS,
    "visualization": VIZ_KEYS,
}


class DataModel(pydantic.BaseModel):
    data: Dict[str, Dict[str, Union[str, bool]]]


class LoadYaml(pydantic.BaseModel):
    """Validation of Dataset YAML."""
    workflow: str
    config_path: Union[str, Path]

    @pydantic.validator("config_path", pre=True)
    @classmethod
    def validate_path(cls, value: Union[str, Path]) -> Path:
        """Validate the configuration file path."""
        path = Path(value)
        if not path.exists():
            raise ValueError(f"{value} does not exist! Please check the path again.")
        return path

    @pydantic.validator("workflow", pre=True)
    @classmethod
    def validate_workflow_name(cls, value: str) -> str:
        """Validate workflow name."""
        valid_workflows = WORKFLOW_KEYS.keys()
        if value not in valid_workflows:
            raise ValueError(f"Invalid workflow: {value}. Please choose one of {', '.join(valid_workflows)}.")
        return value

    def parse_yaml(self) -> Dict[str, Union[str, bool]]:
        """Parse the YAML configuration file for each dataset."""
        with open(self.config_path, 'r') as f:
            data = yaml.safe_load(f)

        # Check missing values in the YAML
        if any(v is None for v in data.values()):
            raise ValueError("All parameters are not defined! Please check the YAML file.")

        # Validate keys against the workflow's expected keys
        self._validate_workflow_keys(data)
        
        return data

    def _validate_workflow_keys(self, data: Dict[str, Union[str, bool]]) -> None:
        """Validate that the keys in the YAML match the expected keys for the selected workflow."""
        # expected_keys = WORKFLOW_KEYS[self.workflow]
        # if data.get("background_correction", False) and set(data.keys()) != expected_keys:
        #     raise ValueError(f"Invalid parameters for {self.workflow} workflow. Expected keys: {expected_keys}")

         # Check for missing required keys
        required_keys = ANALYSIS_KEYS - OPTIONAL_KEYS
        missing_keys = required_keys - data.keys()
        if missing_keys:
            raise ValueError(f"Missing required parameters for {self.workflow} workflow. Missing keys: {missing_keys}")

        # Warn for unrecognized keys (optional, remove if not needed)
        unrecognized_keys = data.keys() - ANALYSIS_KEYS
        if unrecognized_keys:
            print(f"Warning: Unrecognized keys found in the YAML file: {unrecognized_keys}")

        

