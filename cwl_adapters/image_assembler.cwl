$namespaces:
  edam: https://edamontology.org/
$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
class: CommandLineTool
cwlVersion: v1.0
doc: 'This plugin assembles images into a stitched image using an image stitching
  vector.

  https://github.com/PolusAI/polus-plugins/tree/master/transforms/images/image-assembler-plugin'
inputs:
  imgPath:
    doc: Path to input image collection
    inputBinding:
      prefix: --imgPath
    label: Path to input image collection
    type: Directory
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
  stitchPath:
    doc: Path to directory containing "stitching vector" file img-global-positions-0.txt
    inputBinding:
      prefix: --stitchPath
    label: Path to directory containing "stitching vector" file img-global-positions-0.txt
    type: Directory
  timesliceNaming:
    doc: Label images by timeslice rather than analyzing input image names
    inputBinding:
      prefix: --timesliceNaming
    label: Label images by timeslice rather than analyzing input image names
    type: boolean?
label: Image Assembler
outputs:
  assembled_image:
    doc: JSON file with outputs
    format: edam:format_3727
    label: The assembled montage image
    outputBinding:
      glob: '*.ome.tif'
    type: File?
  outDir:
    doc: Output collection
    label: Output collection
    outputBinding:
      glob: $(inputs.outDir.basename)
    type: Directory
  preview_json:
    doc: JSON file with outputs
    format: edam:format_3464
    label: JSON file with outputs
    outputBinding:
      glob: preview.json
    type: File?
requirements:
  DockerRequirement:
    dockerPull: polusai/image-assembler-plugin:1.4.0-dev0
  EnvVarRequirement:
    envDef:
      HOME: /home/polusai
  InitialWorkDirRequirement:
    listing:
    - $(inputs.stitchPath)
    - entry: $(inputs.outDir)
      writable: true
  InlineJavascriptRequirement: {}
  NetworkAccess:
    networkAccess: true
