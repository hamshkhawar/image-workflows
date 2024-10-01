"""CWL Workflow."""
import logging
import typer
from pathlib import Path
from typing import Optional
from image.workflows.utils import LoadYaml
from image.workflows.cwl_analysis import CWLAnalysisWorkflow
from image.workflows.cwl_nuclear_segmentation import CWLSegmentationWorkflow
from image.workflows.cwl_visualization import CWLVisualizationWorkflow




app = typer.Typer()

# Initialize the logger
logging.basicConfig(
    format="%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger("WIC Python API")
logger.setLevel(logging.INFO)


@app.command()
def main(
    name: str = typer.Option(
        ...,
        "--name",
        "-n",
        help="Name of imaging dataset of Broad Bioimage Benchmark Collection (https://bbbc.broadinstitute.org/image_sets)"
    ),
    workflow: str = typer.Option(
        ...,
        "--workflow",
        "-w",
        help="Name of cwl workflow"
    ),
    out_dir: Optional[Path] = typer.Option(
        None,
        "--outDir",
        "-o",
        help="Name of cwl workflow"
    )
) -> None:

    """Execute CWL Workflow."""

    logger.info(f"name = {name}")
    logger.info(f"workflow = {workflow}")
    logger.info(f"outDir = {out_dir}")

    config_path = Path.cwd().joinpath(f"configuration/{workflow}/{name}.yml")
    work_dir = Path.cwd()
 


    model = LoadYaml(workflow=workflow, config_path=config_path)
    params = model.parse_yaml()
    if out_dir == None:
        out_dir = Path.cwd()
    params["out_dir"] = out_dir
    params["work_dir"] = work_dir


    if workflow == "analysis":
        logger.info(f"Executing {workflow}!!!")
        model = CWLAnalysisWorkflow(**params)
        model.workflow()

    if workflow == "segmentation":
        logger.info(f"Executing {workflow}!!!")
        model = CWLSegmentationWorkflow(**params)
        model.workflow()

    # if workflow == "visualization":
    #     logger.info(f"Executing {workflow}!!!")
    #     model = CWLVisualizationWorkflow(**params)
    #     model.workflow()


    logger.info("Completed CWL workflow!!!")


if __name__ == "__main__":
    app()