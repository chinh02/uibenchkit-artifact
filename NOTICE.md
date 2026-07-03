# Third-Party Notices

UIBenchKit is an original integration and orchestration toolkit released under
the MIT License. It implements methods described by the following research and
incorporates the noted third-party code.

## Design2Code Metrics

`UIBenchKit/scripts/metric/Design2Code` contains metric code derived from
`NoviScl/Design2Code` by Chenglei Si and contributors:

- Repository: https://github.com/NoviScl/Design2Code
- Code license: MIT License, Copyright (c) 2023 Chenglei Si
- Dataset license: ODC Attribution License (ODC-By)

No Design2Code benchmark dataset is redistributed in this artifact image.

## Generation Method References

The `latcoder`, `layoutcoder`, and `uicopilot` modules are UIBenchKit
integrations based on the algorithms and prompts described in their respective
papers. They are attributed in the accepted UIBenchKit paper and repository
documentation. No external dataset from those projects is redistributed here.

- LaTCoder: Yi Gui et al., "Converting Webpage Design to Code with
  Layout-as-Thought," KDD 2025.
- LayoutCoder: Fan Wu et al., "MLLM-Based UI2Code Automation Guided by UI
  Layout Information," ISSTA 2025.
- UICopilot: Yi Gui et al., "Automating UI Synthesis via Hierarchical Code
  Generation from Webpage Designs," 2025.
- DCGen: Yuxuan Wan et al., "Divide-and-Conquer: Generating UI Code from
  Screenshots," FSE 2025.

Runtime Python, JavaScript, Chromium, model checkpoints, and container base
images retain their own licenses. Their exact package versions are recorded in
the lockfiles and image metadata.

