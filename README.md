# CORNERSTONE Community Repository

<img src="./docs/_static/CORNERSTONE_Logo.png" class="align-center"
width="600" alt="image" />

Welcome to CORNERSTONE Community repository!

## Aim & Vision

Create an environment where community members can:

- Contribute to a public library of components for the benefit of other
  users
- Hold discussions over improvements on the designs, or alternative
  methodologies
- Form a library of elements that have accessible metadata for easy
  integration into custom codes.

To start contributing, fork the repository (see the guidance on forks &
pull requests through an exemplary submission
[here](./docs/how-to/index.md)). This will give you
access to all of the Community PDK folders. You can populate your
repository without submitting a pull request. Instructions below are
suitable for submission to a single platform. For multi-platform
submissions, cycle through the instructions for each platform.

We aim to incorporate the Community repository into the Wave Photonics
(WP) PDK Management Platfrom. WP has provided guidelines and tests for validation of
the components and supporting metafiles. It is expected from the
Community Members to adhere to the WP metafile format, which are
outlined in the [formatting
guidelines](./docs/guidelines/index.md). Please also see
[Examples](./docs/examples/index.md) for commentary on the WP YAML fields.

## Overview of the repository structure

- `SiN_300nm/`, `Si_220nm_active/`, &c: Folders for platforms that CORNERSTONE offers.
- `<PlatformFolder>/components/`: Contains components for the said platform.
- `<PlatformFolder>/materials/`: Contains refractive index information regarding the materials involved in the said platform.
- `<PlatformFolder>/drc_rules.lydrc`: DRC script for the said platform
- `LICENSE.txt`: License information
- `README.md`: This document
- `docs/`: For generation of the documentation in ReadTheDocs: [cornerstone-community in ReadTheDocs](https://cornerstone-community.readthedocs.io)
- `pyproject.toml`: Dependency list for installation using `uv pip install .[docs, validator]`


## Usage - access

The primary contents of this repository are the GDS files within the respective platform folders (e.g. `SiN_300nm`). The GDS files can be found within the `components` folder within each platform directory, alongside `*.yaml` files that contain information on port arrangement of the components. The port files are primarily for use during exports, the components GDS files can be accessed without interacting with the `*.yaml` files.

In the near future, we will populate the platform folders with experimental and simulation data for supplementary use of the repository users.

## Usage - contribution

### Submission format

**Basic**

1. Place the new GDS files for your components, with naming convention `<Platform>_<Wavelength>_<ComponentName>.gds` into `components` folder of the platform folder.
2. Submit a pull request using the Basic pull request template.

**Advanced**

1.  Place the new GDS files for your components, with naming convention
    `<Platform>_<Wavelength>_<ComponentName>.gds` into `components`
    folder of the platform folder.
2.  Create a YAML file for each component. You can base the component
    YAML on the existing YAMLs of similar components ([see
    examples](./docs/examples/index.md)) . If a new port cross-section is needed
    in the YAML, put a placeholder for the new port for now.
3.  Create the GDS file for the new cross section in `cross-sections`
    folder. The GDS file will contain a structure 50um long in x-axis,
    and has the linear cross section along y-axis. The name of the GDS
    file will be the name of the cross-section.
4.  Append the new cross-section metadata into the `cross_sections.yaml`
    file within `cross-sections` folder.
5.  Within the Component YAMLs, you may specify your name/alias and
    email as an author - otherwise we can also assign design credits to
    your GitHub username. A component or a file can have more than one
    author.
6.  Include the ancestry of the component in the Component YAML file.
    The ancestry should include the prior component(s) that the new
    component is based on. One level of ancestry is sufficient.
7.  Submit a pull request using the Advanced pull request template.

**Documentation**
1.  Following the new entries/modifications, submit a pull request using Documentation pull request template.
2.  Provide a list of documentation updates and related information.

### Submission acceptance stages

The initial version is comprised of components that have been previously
fabricated and characterised. We aim to make the characterisation
results public as soon as possible.

We expect the new component submissions to follow a verification flow:

1.  Community member submits a new design file, either an original file
    made publicly available by the user, or a modification to an
    already-existing component within the Community repository.
2.  The submission will be reviewed by the CORNERSTONE team for
    compliancy with the licensing and export policies. If the submission
    is rejected, a detailed feedback will be provided to the
    contributor.
3.  If the designs are accepted, they will be will be made available in
    the repository for the use of the Community as an alpha version,
    without experimental verification.
4.  A test batch will be fabricated alongside confirmed components for
    characterisation of the new submission.
5.  Provided the functionality of the components is confirmed, it will
    be incorporated into the stable version of the Community.
6.  Components whose functionalities couldn't be verified will be sent
    back to the contributor alongside experimental data and feedback.

## License

The CORNERSTONE Community repository is licensed with [TAPR Open
Hardware License](https://tapr.org/the-tapr-open-hardware-license/)

## Contact

[Contact us](mailto:pdk.cornerstone@soton.ac.uk) for questions related
to the your Community submissions, Community repository contents - or
any other issues related to the Community repository.
