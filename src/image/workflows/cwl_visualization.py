import logging
from pathlib import Path
import typing
import subprocess
import os
from sophios.api.pythonapi import Step, Workflow
from image.workflows.utils import OUT_PATH, SUBMIT_JOBS
from image.workflows.baseclass import CWLWorkflowBase


# Initialize the logger
logger = logging.getLogger(__name__)
RUN_WORKFLOW = os.environ.get("RUN_WORKFLOW", "local")


class CWLVisualizationWorkflow(CWLWorkflowBase):
    """
    A CWL visualization pipeline to process imaging datasets.
    
    Attributes:
        work_dir: Path to working directory.
        name: Name of the imaging dataset.
        file_pattern: Pattern for parsing raw filenames.
        out_file_pattern: Desired format for output filenames.
        layout : A list indicating the grid layout.
        pyramid_type : A list indicating the grid layout.
        ff_pattern: Filename pattern for selecting flatfield components.
        df_pattern: Filename pattern for selecting darkfield components.
        group_by: Variables used for grouping the file pattern.
        background_correction: Flag to enable background correction.
        map_directory: Enable mapping of folder names.
        out_dir: Directory for saving outputs.
    """
    ATTRIBUTE_MAP = {
        "work_dir":"work_dir",
        "name":"name",
        "inp_dir":"inp_dir",
        "file_pattern": "file_pattern",
        "out_file_pattern": "out_file_pattern",
        "layout": "layout",
        "pyramid_type": "pyramid_type",
        "image_type": "image_type",
        "ff_pattern": "ff_pattern",
        "df_pattern": "df_pattern",
        "group_by": "group_by",
        "map_directory": "map_directory",
        "background_correction": "background_correction",
        "container_engine": "containerEngine",
        "out_dir": "out_dir"
    }
    def __init__(
        self,
        work_dir: Path,
        name: str,
        inp_dir:Path,
        file_pattern: str,
        out_file_pattern: str,
        layout: str,
        pyramid_type: str,
        image_type: str,
        ff_pattern: typing.Optional[str] = '',
        df_pattern: typing.Optional[str] = '',
        group_by: typing.Optional[str] = '',
        map_directory: typing.Optional[bool] = False,
        background_correction: typing.Optional[bool] = False,
        container_engine:typing.Optional[str]="singularity",
        out_dir: typing.Optional[Path] = OUT_PATH
    ):
        super().__init__(work_dir, name, inp_dir, file_pattern, out_file_pattern, container_engine, out_dir)
        for attr, _ in self.ATTRIBUTE_MAP.items():
            setattr(self, attr, locals()[attr])

    def set_parameters(self, step, **kwargs):
        """
        Dynamically set parameters for a CWL step.
        """
        for attr, param_key in self.ATTRIBUTE_MAP.items():
            if attr in kwargs:
                setattr(step, param_key, kwargs[attr])

    def workflow(self) -> None:
        """
        A CWL visualization pipeline.
        """
        ## Step: File Renaming
        rename = self.create_step(self._get_manifest_url("file_renaming"))
        rename.filePattern = self.file_pattern
        rename.outFilePattern = self.out_file_pattern
        rename.mapDirectory = self.map_directory
        rename.inpDir = self.inp_dir
        rename.outDir = Path("rename.outDir")

        ## Step: OME Converter
        ome_converter = self.create_step(self._get_manifest_url("ome_converter"))
        ome_converter.filePattern = self.out_file_pattern
        ome_converter.inpDir = rename.outDir
        ome_converter.outDir = Path("ome_converter.outDir")

        # ## Optional: Background correction

        file_pattern = self.image_pattern(self.out_file_pattern)

        if self.background_correction:
            estimate_flatfield = self.create_step(self._get_manifest_url("estimate_flatfield"))
            estimate_flatfield.inpDir = ome_converter.outDir
            estimate_flatfield.filePattern = file_pattern
            estimate_flatfield.groupBy = self.group_by
            estimate_flatfield.getDarkfield = True
            estimate_flatfield.outDir = Path("estimate_flatfield.outDir")

            apply_flatfield = self.create_step(self._get_manifest_url("apply_flatfield"))
            apply_flatfield.imgDir = ome_converter.outDir
            apply_flatfield.imgPattern = file_pattern
            apply_flatfield.ffDir = estimate_flatfield.outDir
            apply_flatfield.ffPattern = self.ff_pattern
            apply_flatfield.dfPattern = self.df_pattern
            apply_flatfield.outDir = Path("apply_flatfield.outDir")


        # Montage
        montage = self.create_step(self._get_manifest_url("montage_url"))
        montage.inpDir = apply_flatfield.outDir if self.background_correction else ome_converter.outDir
        montage.filePattern = file_pattern
        montage.layout = self.layout
        montage.imageSpacing = '1'
        montage.gridSpacing = '20'
        montage.outDir = Path("montage.outDir")
    

        # # Image Assembler
        image_assembler = self.create_step(
            self._get_manifest_url("image_assembler_url")
        )
        image_assembler.imgPath = apply_flatfield.outDir if self.background_correction else ome_converter.outDir
        image_assembler.stitchPath =  montage.outDir
        image_assembler.outDir = Path("image_assembler.outDir")
        

        # Precompute Slide
        precompute_slide = self.create_step(
            self._get_manifest_url("precompute_slide_url")
        )
        precompute_slide.pyramidType = self.pyramid_type
        precompute_slide.imageType = self.image_type
        precompute_slide.inpDir = image_assembler.outDir
        precompute_slide.outDir = Path("precompute_slide.outDir")


        logger.info("Initiating CWL Visualization Workflow!!!")
        steps = [
            rename,
            ome_converter,
            estimate_flatfield if self.background_correction else None,
            apply_flatfield if self.background_correction else None,
            montage,
            image_assembler,
            precompute_slide
        ]
        # Assuming self.inp_dir is a Path object
        platename = Path(self.inp_dir).name.replace(" ", "")
        workflowname = f"{self.name}_{platename}_viz_workflow"
        

        if self.container_engine == "singularity":
            args = ['--container_engine',self.container_engine]
            args += ['--cwl_runner', 'toil-cwl-runner']
            workflow = Workflow(steps,  workflowname, args)
        else:
            workflow = Workflow(steps,  workflowname)


        # Compile and run using WIC python API
        workflow.compile()
        workflow.run()

        # if RUN_WORKFLOW == "local":
        #     # Run using WIC python API
        #     workflow.run()

        # if RUN_WORKFLOW == "sbatch":
        #     # Save WIC workflow on a disk
        #     workflow.write_ast_to_disk(self.wic_path)

        #     wic_file = self.wic_path.joinpath(f"{workflowname}.wic")
            
        #     subprocess.run([SUBMIT_JOBS, wic_file, OUT_PATH], check=True)

        logger.info("Completed CWL visualization workflow.")
        return