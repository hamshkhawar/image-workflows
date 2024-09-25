$namespaces:
  edam: https://edamontology.org/
$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
class: CommandLineTool
cwlVersion: v1.0
doc: 'This WIPP plugin converts BioFormats supported data types to the OME Zarr file
  format.

  https://github.com/PolusAI/polus-plugins/tree/master/formats/ome-converter-plugin'
inputs:
  fileExtension:
    default: default
    doc: The file extension
    inputBinding:
      prefix: --fileExtension
    label: The file extension
    type: string
  filePattern:
    doc: A filepattern, used to select data for conversion
    inputBinding:
      prefix: --filePattern
    label: A filepattern, used to select data for conversion
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
label: OME Zarr Converter
outputs:
  outDir:
    doc: Output collection
    label: Output collection
    outputBinding:
      glob: $(inputs.outDir.basename)
    type: Directory
requirements:
  DockerRequirement:
    dockerPull: polusai/ome-converter-plugin:0.3.2-dev2
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
