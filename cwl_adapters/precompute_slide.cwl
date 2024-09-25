$namespaces:
  edam: https://edamontology.org/
$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
class: CommandLineTool
cwlVersion: v1.0
doc: 'This plugin generates image pyramids in multiple viewing formats.

  https://github.com/PolusAI/polus-plugins/tree/master/visualization/polus-precompute-slide-plugin'
inputs:
  filePattern:
    doc: Filename pattern used to parse data
    inputBinding:
      prefix: --filePattern
    label: Filename pattern used to parse data
    type: string?
  imageType:
    doc: Image is either Segmentation or Image
    inputBinding:
      prefix: --imageType
    label: Image is either Segmentation or Image
    type: string
  inpDir:
    doc: Input generic data collection to be processed by this plugin
    inputBinding:
      prefix: --inpDir
    label: Input generic data collection to be processed by this plugin
    type: Directory
  outDir:
    doc: Output collection
    inputBinding:
      prefix: --outDir
    label: Output collection
    type: Directory
  pyramidType:
    doc: Build a DeepZoom, Neuroglancer, Zarr pyramid
    inputBinding:
      prefix: --pyramidType
    label: Build a DeepZoom, Neuroglancer, Zarr pyramid
    type: string
label: Precompute Slide
outputs:
  outDir:
    doc: Output collection
    label: Output collection
    outputBinding:
      glob: $(inputs.outDir.basename)
    type: Directory
requirements:
  DockerRequirement:
    dockerPull: polusai/precompute-slide-plugin:1.7.0-dev0
  EnvVarRequirement:
    envDef:
      HOME: /home/polusai
  InitialWorkDirRequirement:
    listing:
    - entry: $(inputs.outDir)
      writable: true
  InlineJavascriptRequirement: {}
  NetworkAccess:
    networkAccess: true
