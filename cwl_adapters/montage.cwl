$namespaces:
  edam: https://edamontology.org/
$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
class: CommandLineTool
cwlVersion: v1.0
doc: 'This plugin generates a stitching vector that will montage images together.

  https://github.com/PolusAI/polus-plugins/tree/master/transforms/images/montage-plugin'
inputs:
  filePattern:
    doc: Filename pattern used to parse data
    inputBinding:
      prefix: --filePattern
    label: Filename pattern used to parse data
    type: string
  flipAxis:
    doc: Axes to flip when laying out images
    inputBinding:
      prefix: --flipAxis
    label: Axes to flip when laying out images
    type: string?
  gridSpacing:
    doc: Specify spacing between images in the lowest grid
    inputBinding:
      prefix: --gridSpacing
    label: Specify spacing between images in the lowest grid
    type: int?
  imageSpacing:
    doc: Specify spacing multiplier between grids
    inputBinding:
      prefix: --imageSpacing
    label: Specify spacing multiplier between grids
    type: int?
  inpDir:
    doc: Input image collection to be processed by this plugin
    inputBinding:
      prefix: --inpDir
    label: Input image collection to be processed by this plugin
    type: Directory
  layout:
    doc: Specify montage organization
    inputBinding:
      prefix: --layout
    label: Specify montage organization
    type: string?
  outDir:
    doc: Output collection
    inputBinding:
      prefix: --outDir
    label: Output collection
    type: Directory
  preview:
    doc: Generate a JSON file describing what the outputs should be
    inputBinding:
      prefix: --preview
    label: Generate a JSON file describing what the outputs should be
    type: boolean?
label: Montage
outputs:
  global_positions:
    doc: The "stitching vector", i.e. the positions of the individual images in the
      montage
    label: The "stitching vector", i.e. the positions of the individual images in
      the montage
    outputBinding:
      glob: $(inputs.outDir.basename)/img-global-positions-0.txt
    type: File?
  outDir:
    doc: Output collection
    label: Output collection
    outputBinding:
      glob: $(inputs.outDir.basename)
    type: Directory
  preview_json:
    doc: JSON file describing what the outputs should be
    format: edam:format_3464
    label: JSON file describing what the outputs should be
    outputBinding:
      glob: preview.json
    type: File?
requirements:
  DockerRequirement:
    dockerPull: polusai/montage-plugin:0.5.0
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
