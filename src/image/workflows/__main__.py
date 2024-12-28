"""CWL Workflow Script.

This script provides a command-line interface (CLI) for executing various CWL workflows,
including analysis, segmentation, and visualization. It uses Typer for CLI argument parsing
and logging for tracking the workflow execution.

Usage:
    python -m image.workflows --name <dataset_name> --workflow <workflow_name> [--outDir <output_directory>]

Example:
    python -m image.workflows --name SOD1 --workflow visualization --outDir /path/to/output
"""

import logging
import typer
from pathlib import Path
from typing import Optional
from image.workflows.utils import LoadYaml
from image.workflows.cwl_analysis import CWLAnalysisWorkflow
from image.workflows.cwl_nuclear_segmentation import CWLSegmentationWorkflow
from image.workflows.cwl_visualization import CWLVisualizationWorkflow
import copy

app = typer.Typer()

# Initialize the logger
logging.basicConfig(
    format="%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger("WIC Python API")
logger.setLevel(logging.INFO)

def process_plate(workflow:str, params:dict, plate:Path):
    """Process a single plate using the specified workflow.

    Args:
        args (tuple): A tuple containing the workflow name, parameters, and plate name.
    """
    # workflow, params, plate = args
    try:
        logger.info(f"Processing plate: {plate} for workflow: {workflow}")

        if workflow in ["analysis", "anlys"]:
            logger.info(f"Running analysis workflow for {plate}")
            model = CWLAnalysisWorkflow(**params)
            model.workflow()

        elif workflow in ["segmentation", "seg"]:
            logger.info(f"Running segmentation workflow for {plate}")
            model = CWLSegmentationWorkflow(**params)
            model.workflow()

        elif workflow in ["visualization", "viz"]:
            logger.info(f"Running visualization workflow for {plate}")
            local_params = copy.deepcopy(params)  # Ensure params are not shared
            local_params["inp_dir"] = plate
            model = CWLVisualizationWorkflow(**local_params)
            model.workflow()

        logger.info(f"Completed plate: {plate}")
    except Exception as e:
        logger.error(f"Error processing plate {plate}: {e}")

def update_workflow_name(workflow: str) -> str:
    """Replace 'viz' with 'visualization' in the given path."""
    if workflow == "viz":
        workflow = "visualization"
    elif workflow == "seg":
        workflow = "segmentation"
    elif workflow == "anlys":
        workflow = "analysis"
    else:
        workflow = workflow

    return workflow

@app.command()
def main(
    name: str = typer.Option(
        ...,
        "--name",
        "-n",
        help="Name of imaging dataset"
    ),
    workflow: str = typer.Option(
        ...,
        "--workflow",
        "-w",
        help="Name of CWL workflow"
    ),
    out_dir: Optional[Path] = typer.Option(
        None,
        "--outDir",
        "-o",
        help="Output directory for the workflow results"
    )
) -> None:
    """Execute CWL Workflow.

    This function initializes the workflow parameters, reads the plate names, and processes
    each plate using the specified workflow.

    Args:
        name (str): Name of the imaging dataset.
        workflow (str): Name of the CWL workflow to execute.
        out_dir (Optional[Path]): Directory to store the workflow results.
    """
    logger.info(f"name = {name}")
    logger.info(f"workflow = {workflow}")
    logger.info(f"outDir = {out_dir}")

    workflow = update_workflow_name(workflow)

    config_path = Path.cwd().joinpath(f"configuration/{workflow}/{name}.yml")
   
    plates_path = Path.cwd().joinpath(f"plates/{name}_plates.txt")

    # Read the file into a list
    with open(plates_path, 'r') as file:
        plates = [line.strip() for line in file.readlines()]

    work_dir = Path.cwd()

    model = LoadYaml(workflow=workflow, config_path=config_path)
    params = model.parse_yaml()

    if out_dir is None:
        out_dir = Path.cwd()
    

    # Prepare arguments

    for plate in plates:
        params["out_dir"] = out_dir
        params["work_dir"] = work_dir
        params["inp_dir"] = plate
        process_plate(workflow, params, plate)

    logger.info("Completed CWL workflow!!!")

if __name__ == "__main__":
    app()