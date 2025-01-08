class: CommandLineTool
cwlVersion: v1.2
inputs:
  channelName:
    inputBinding:
      prefix: --channelName
    type: string
  features:
    inputBinding:
      prefix: --features
    type: string?
  filePattern:
    inputBinding:
      prefix: --filePattern
    type: string
  groupBy:
    inputBinding:
      prefix: --groupBy
    type: string
  inpDir:
    inputBinding:
      prefix: --inpDir
    type: Directory
  metaCols:
    inputBinding:
      prefix: --metaCols
    type: string?
  metaDir:
    inputBinding:
      prefix: --metaDir
    type: Directory?
  outDir:
    inputBinding:
      prefix: --outDir
    type: Directory
  plateName:
    inputBinding:
      prefix: --plateName
    type: string?
  preview:
    inputBinding:
      prefix: --preview
    type: boolean?
outputs:
  outDir:
    outputBinding:
      glob: $(inputs.outDir.basename)
    type: Directory
requirements:
  DockerRequirement:
    dockerPull: polusai/tabular-feature-concat-tool:0.1.0-dev4
  InitialWorkDirRequirement:
    listing:
    - entry: $(inputs.outDir)
      writable: true
  InlineJavascriptRequirement: {}
  ResourceRequirement:
    ramMin: 10240
  NetworkAccess:
    networkAccess: true
baseCommand: ['python3', '-m', 'polus.tabular.transforms.feature_concat']
