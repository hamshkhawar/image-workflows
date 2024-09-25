$namespaces:
  edam: https://edamontology.org/
$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
class: CommandLineTool
cwlVersion: v1.0
doc: 'Rename and store image collection files in a new image collection

  https://github.com/PolusAI/polus-plugins/tree/master/formats/file-renaming-plugin'
inputs:
  filePattern:
    inputBinding:
      prefix: --filePattern
    type: string
  inpDir:
    inputBinding:
      prefix: --inpDir
    type: Directory
  mapDirectory:
    inputBinding:
      prefix: --mapDirectory
    type: string?
  outDir:
    doc: Output collection
    inputBinding:
      prefix: --outDir
    label: Output collection
    type: Directory
  outFilePattern:
    inputBinding:
      prefix: --outFilePattern
    type: string
  preview:
    doc: Generate a JSON file describing what the outputs should be
    inputBinding:
      prefix: --preview
    label: Generate a JSON file describing what the outputs should be
    type: boolean?
label: File Renaming
outputs:
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
    dockerPull: polusai/file-renaming-plugin:0.2.1-dev0
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
