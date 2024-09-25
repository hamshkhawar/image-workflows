$namespaces:
  cwltool: http://commonwl.org/cwltool#
  edam: https://edamontology.org/
$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
class: CommandLineTool
cwlVersion: v1.0
doc: 'This WIPP plugin will take a collection of images and use the BaSiC flatfield
  correction algorithm to generate a flatfield image, a darkfield image, and a photobleach
  offset.

  https://github.com/PolusAI/polus-plugins/tree/master/regression/basic-flatfield-estimation-plugin'
hints:
  cwltool:CUDARequirement:
    cudaComputeCapabilityMin: '3.0'
    cudaDeviceCountMax: 1
    cudaDeviceCountMin: 1
    cudaVersionMin: '11.4'
inputs:
  filePattern:
    doc: File pattern to subset data
    inputBinding:
      prefix: --filePattern
    label: File pattern to subset data
    type: string?
  getDarkfield:
    doc: If 'true', will calculate darkfield image
    inputBinding:
      prefix: --getDarkfield
    label: If 'true', will calculate darkfield image
    type: boolean?
  groupBy:
    doc: Variables to group together
    inputBinding:
      prefix: --groupBy
    label: Variables to group together
    type: string?
  inpDir:
    doc: Path to input images
    inputBinding:
      prefix: --inpDir
    label: Path to input images
    type: Directory
  outDir:
    doc: Output image collection
    inputBinding:
      prefix: --outDir
    label: Output image collection
    type: Directory
  preview:
    doc: Generate a JSON file describing what the outputs should be
    inputBinding:
      prefix: --preview
    label: Generate a JSON file describing what the outputs should be
    type: boolean?
label: BaSiC Flatfield Estimation
outputs:
  outDir:
    doc: Output image collection
    label: Output image collection
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
    dockerPull: polusai/basic-flatfield-estimation-plugin:2.1.1
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
