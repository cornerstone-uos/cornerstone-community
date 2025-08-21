# Formatting guidelines for the GDS files and metafiles

Cornerstone collaborates with [Wavephotonics](https://wavephotonics.com)
to export its PDKs to EDA tools. We use the building block verification
tools created by Wavephotonics, and require some of the metafiles from
the Community Members as part of the submission process. Multiple
metafile format exists within the infividual PDK folders, which are
explained below and with provided examples.

## Formatting guidelines for the submission files

A minimal submission would include a component GDS file for an
individual component, and a YAML metafile accompanying it for the
component description. These component files would need to be placed
within the `components` directory of the platform folder it belongs to
(e. g. `Si_220nm_active/components/`). For an introduction to the file
format, see the [example on YAML format](../examples/Ex0_YAMLFormat.md).
The Component YAML format is also explained step-by-step in [Component
YAML format - Example 1](../examples/Ex1_ComponentYAML.md).

If the submitted component contains ports that have cross-sections
different than the ones defined in `cross-sections` folder of the
platform (e. g. `Si_220nm_active/cross-sections/`), then the new
cross-section will be required as a GDS file, alongside a new
cross-section entry within `cross-sections/cross_sections.yaml`
metafile. An example Cross-section YAML file can be seen in
[Cross-section YAML format - Example
2](../examples/Ex2_CrossSectionYAML.md).

Additional YAML fields that we would like to see included in the new
components within Submissions are described in [Additional YAML
Fields](../examples/Additional_YAML_Fields.md). These fields include a
`description` for the component, a list of `ancestor` building blocks
the Component is based on, and `author` information for communication
and design credits.

Aside from these, the Community Members do not need to include any other
files in their submission. However, the inclusigon of numerical and
experimental data regarding the functionality of the components are
encouraged. This can also be made through [contacting
us](mailto:pdk.cornerstone@soton.ac.uk) about the Submission.

The submitted components must obey to the fabrication process detailed
within the Design Guidelines for the specific platform. These details
can also be found within the metafiles inside the platform folder,
especially in `process_overview.yaml`, `drc_rules.lydrc`,
`materials\*.csv`, `floorplans\floorplans.yaml`. The explanation of
these metafiles can be found in [Appendix](../Appendix.md).