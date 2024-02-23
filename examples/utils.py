import json
import pydantic
from pathlib import Path
from typing import Dict

GITHUB_TAG = "https://raw.githubusercontent.com"


class DataModel(pydantic.BaseModel):
    data: Dict[str, Dict[str, str]]


def get_params(path: Path, name: str):
    """Loading json file for getting parameters"""
    with open(path) as json_file:
        # Read the JSON data
        data = json.load(json_file)
    params = [v[name] for k, v in data.items()][0]
    return params


seg_params = {
    "BBBC039": {
        "name": "BBBC039",
        "file_pattern": ".*_{row:c}{col:dd}_s{s:d}_w{channel:d}.*.tif",
        "out_file_pattern": "x{row:dd}_y{col:dd}_p{s:dd}_c{channel:d}.tif",
        "image_pattern": "images_x{x:dd}_y{y:dd}_p{p:dd}_c{c:d}.ome.tif",
        "map_directory": "raw",
        "ff_pattern": "images_x\\(00-15\\)_y\\(01-24\\)_p0\\(1-9\\)_c{c:d}_flatfield.ome.tif",
        "df_pattern": "images_x\\(00-15\\)_y\\(01-24\\)_p0\\(1-9\\)_c{c:d}_darkfield.ome.tif",
        "group_by": "c",
    }
}
model = DataModel(data=seg_params)
model_dict = model.dict()

json_dir = Path(Path(__file__).parents[1]).joinpath("bbbc_json")
json_dir.mkdir(parents=True, exist_ok=True)
JSON_FILENAME = json_dir.joinpath("bbbc_segconfig.json")

with Path.open(JSON_FILENAME, "w") as json_file:
    json.dump(model_dict, json_file, indent=2)
