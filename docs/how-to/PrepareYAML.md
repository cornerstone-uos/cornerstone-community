# How to prepare the YAML for a component GDS?

Below is a step-by-step guide for preparing the YAML file for a component.

## Basic component - Photodetector

Create a YAML file and start by setting the name and component type.

``` yaml
name: SOI220nm_1550nm_TE_IsolatedDetector
component_type: Photodiode
```

Define the ports. Each port definition should contain:
- port name
- port type 
- port location
- port orientation
- port cross section (or width)
- mode information on the port (if the port is non-electrical)


Below, we have defined the leftmost optical port as ```o1```:

``` yaml
ports:
- name: o1
  port_type: optical
  center:
  - 0
  - 0
  orientation: 180
  cross_section: rib_1550nm_TE
  modes:
  - mode_numbers:
    - 0
    - 0
    polarisation: TE
    wavelength: 1550
```

Allowed ```port_type```s can be found in [ports list](../references/ports_list.md).

```center``` is a two-element (x,y) array.

```orientation``` is the counter-clockwise angle the port is facing towards in degrees - here, it is facing -x direction, hence its angle is equal to 180.

```cross_section``` is the cross-section information of the port. These are defined in the ```cross-sections``` folder in each platform. Using appropriate cross-section information prevents port mismatches during component connections (i.e. connections with different cross-sections on two sides can be detected)

```modes``` contains information regarding the polarisation, wavelength and mode index for the operation mode. Here, mode (0,0) corresponds to TE_00 mode.

The electrical ports from the detector can be defined similarly:

``` yaml
- name: e1
  port_type: electrical_rf
  center:
  - 220
  - -142.50000
  orientation: 270
  cross_section: detector
  ```

  We have used ```electrical_rf``` as the port type as this port is expected to contain high-speed electrical signals. Additionally, ```detector``` cross-section is used as defined in the cross-sections folder ([see original](../../Si_220nm_active/cross-sections/cross_sections.yaml))

  If all the optical ports (```port_type``` either ```optical```,```vertical_te```,```vertical_tm```,```edge```) share the same ```modes``` structure, instead of defining ```modes``` within each port entry, we can define it on a higher level. 

  ``` yaml
  name: SOI220nm_1550nm_TE_IsolatedDetector
component_type: Photodiode
modes:
- mode_numbers:
  - 0
  - 0
  polarisation: TE
  wavelength: 1550
ports:
- name: e1
  port_type: electrical_rf
  center:
  - 220
  - -142.50000
  orientation: 270
  cross_section: detector
- name: e2
  port_type: electrical_rf
  center:
  - 742
  - -92.5
  orientation: 270
  cross_section: detector
- name: o1
  port_type: optical
  center:
  - 0
  - 0
  orientation: 180
  cross_section: rib_1550nm_TE
- name: o2
  port_type: optical
  center:
  - 1900
  - 0
  orientation: 0
  cross_section: rib_1550nm_TE
  ```

  ## Basic component - Grating coupler

  A grating coupler contains vertical optical ports, which do not have a well-defined cross-section. Below is the YAML file for ```SOI220nm_1550nm_TE_STRIP_Grating_Coupler```:

  ``` yaml
name: SOI220nm_1550nm_TE_STRIP_Grating_Coupler
component_type: GratingCoupler1D
ports:
- name: o1
  port_type: optical
  center:
  - 0
  - 0
  orientation: 180
  cross_section: strip_1550nm
  modes:
  - mode_numbers:
    - 0
    - 0
    polarisation: TE
    wavelength: 1550
- name: vertical_te
  port_type: vertical_te
  center:
  - 369.084
  - 0
  orientation: 0
  width: 10
  coupling_angle_cladding: 6.886
  fibre_modes:
  - fibre_type: SMF-28
    wavelength:   1550.0
```

Notice the differences in ```vertical_te``` port definitions:

- Instead of a cross-section, we are defining a ```width```
- A coupling angle is defined for the cladding. As this component is expected to couple light to a 10°-inclined fibre over a silicon dioxide cladding (n ~ 1.448), the coupling angle is now defined as ```arcsin(sin(10°)/1.448)=6.886°``` 
- Instead of ```modes```, we have ```fibre_modes```, which contains ```fibre_type``` and ```wavelength``` as sub-fields (see [fibre types](../references/fibres_list.md))

Regarding the centre position of a grating coupler, we usually define as the centre of mass for the gratings. This can be calculated automatically during cell generation, or can be found using the cell bounding box macro in KLayout. For details on setting up this macro and its use, please see [Cell bounding box macro](../cellbbox_use.md)

## Derived component example

For a compound component that contains other documented components, we require used component information for version control and modification history.

``` yaml
# define component type, port info, etc; then:
description: Component description
ancestors:
- name: Ancestor_Component_Name_1
  commit: HashKey_of_SourceCommit
  modifications: Any sort of modifications
- name: Ancestor_Component_Just_Included
  commit: ReferenceWithinCommit
authors:
- name: Name Surname or Alias
  organisation: Organisation Formal Name, is Optional
  email: Contributor Email
```

The `description` field explains the functionality and operation principle of the component.

An `ancestor` is the closest relative(s) of the contributed Component, i. e. the building blocks the Component is directly based off of. A component might have multiple ancestors or it can have none; it can also have ancestors as part of the same Contributor Submission. `modifications` can be `none` (the ancestor might have been used directly/translated/rotated), or can include modifications where the component shape was not preserved. We expect the Contributors to define the `ancestor`s in the most direct, plain way.

`authors` are practically the Contributors and any other people who can claim design credits about the component. While the `organisation` field is optional, an `email` field is required for communication purposes. If the Contributors desire to do so, they can specify an alias (like a GitHub user name) as the `name` field.

Below is an example, a standalone light detector within `Si_220nm_active` platform that is built with a grating coupler and the detector from before ([SOI220nm_1550nm_TE_Defect_Detector](../../Si_220nm_active/components/SOI220nm_1550nm_TE_Defect_Detector.yaml))

``` yaml
name: SOI220nm_1550nm_TE_Defect_Detector
component_type: Photodiode
description: Standalone c-band light detector comprised of a defect detector fed by an input grating coupler, also connected to another GC at the transmission port. 
modes:
- mode_numbers:
  - 0
  - 0
  polarisation: TE
  wavelength: 1550
ports:
- name: e1
  port_type: electrical_rf
  center:
  - 542
  - -92.5
  orientation: 270
  cross_section: detector
- name: e2
  port_type: electrical_rf
  center:
  - 742
  - -92.5
  orientation: 270
  cross_section: detector
- name: vertical_te_w
  port_type: vertical_te
  center:
  - 27.915
  - 50
  orientation: 180
  width: 10
  coupling_angle_cladding: 6.886
  fibre_modes:
  - fibre_type: SMF-28
    wavelength: 1550.0
- name: vertical_te1_e
  port_type: vertical_te
  center:
  - 2766.084
  - 50
  orientation: 0
  width: 10
  coupling_angle_cladding: 6.886
  fibre_modes:
  - fibre_type: SMF-28
    wavelength: 1550.0
ancestors:
- name: SOI220nm_1550nm_TE_IsolatedDetector
  commit: ReferenceWithinCommit
  modification: none
- name: SOI220nm_1550nm_TE_RIB_Grating_Coupler
  commit: ReferenceWithinCommit
  modification: none
authors:
- name: H Bilge Yagci
  organisation: Cornerstone / ORC
  email: hby1r25@soton.ac.uk
```

Here, we see that the `SOI220nm_1550nm_TE_Defect_Detector` is built on `SOI220nm_1550nm_TE_IsolatedDetector` and `SOI220nm_1550nm_TE_RIB_Grating_Coupler`. As these ancestors are submitted within the same commit as `SOI220nm_1550nm_TE_Defect_Detector`, the `commit` field for both ancestors were set to `ReferenceWithinCommit`. The ancestors were incorporated directly without modification, hence the `modification` fields are set to `none` (alternatively these can be removed, as queries for `modification` field will return `None`)

We require the inclusion of the ancestor information and author information as it is dictated by our license. By tracking the ancestors across commits, we satisfy the Contributor responsibility to provide before/after versions of the "documentation" files (GDS and metafiles), as well as the modification changes.



