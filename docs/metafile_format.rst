Formatting guidelines for the GDS files and metafiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cornerstone collaborates with `Wavephotonics <https://wavephotonics.com>`_ to export its PDKs to EDA libraries. We use the building block verification tools created by Wavephotonics, and require some of the metafiles from the Community Members as part of the submission process.  Multiple metafile format exists within the infividual PDK folders. An explanation of the required files will be given here, and the other metafiles for compliance with Wavephotonics workflow will be explained in the Appendix.

Formatting guidelines for the submission files
==============================================

A minimal submission would include a component GDS file for an individual component, and a YAML metafile accompanying it for the component description. These component files would need to be placed within the ``components`` directory of the platform folder it belongs to (e. g. ``Si_220nm_active/components/``). For an introduction to the file format, see the `example on YAML format <./examples/Ex0_YAMLFormat.rst>`_. The Component YAML format is also explained step-by-step in 
`Component YAML format - Example 1 <./examples/Ex1_ComponentYAML.rst>`_.

If the submitted component contains ports that have cross-sections different than the ones defined in ``cross-sections`` folder of the platform (e. g. ``Si_220nm_active/cross-sections/``), then the new cross-section will be required as a GDS file, alongside a new cross-section entry within ``cross-sections/cross_sections.yaml`` metafile. An example Cross-section YAML file can be seen in `Cross-section YAML format - Example 2 <./examples/Ex2_CrossSectionYAML.rst>`_.

We would also classify the components based on their Maturity Index within the Component YAML. At the moment, the maturity levels for the components are:
- Level 1: Component defined solely based on electromagnetic simulations. Interconnect-level simulations are not required but they are good-to-have.
- Level 2: The components have been fabricated in a research setting and its results published within an open-access journal, its functionality has been verified (partially or fully).
- Level 3: Component shown to work in 8-inch scale process fabricated within CORNERSTONE, its performance metrics having expected values not dissimilar from the simulated cases, across mutliple chips within a single run.
- Level 4: Component shown to work in 8-inch process flow, across at least 5 runs, with mean performance metrics similar to expected from the simulations.

For each Maturity Index, we would require accompanying numerical or experimental data from the Contributor:
- Level 1: A document explaining/demonstrating the functionality of the component alongside simulation results, in presentation or PDF format.
- Level 2: DOI of the publication mentioned in the Component YAML. A commented document will be requested if the publication and/or its Supplementary Information are not sufficient to verify the performance experimentally. 
- Level 3: Experimental data from multiple chips within the run, compiled into a report that contains the histogram of performance metrics across the fabricated components.
- Level 4: Same as Level 3, with data range expanded to include chips across mutliple chips and MPW runs.

After Level 2 MI, CORNERSTONE will regularly include the Community Components in their characterisation runs to increase their MI.

Aside from these, the Community Members do not need to include any other files in their submission. 

The submitted components must obey to the fabrication process detailed within the Design Guidelines for the specific platform. These details can also be found within the metafiles inside the platform folder, especially in ``process_overview.yaml``, ``drc_rules.lydrc``, ``materials\*.csv``, ``floorplans\floorplans.yaml``. The explanation of these metafiles can be found in `Appendix <./wp_format/Appendix.rst>`_


Component naming convention:
-----------------------------
.. The component names should be appended by a unique identifier. This identifier will be temporary prior to the approval so we can use a basic hash algorithm such as SHA-1. The resultant hash key can be appended to the component name. As an example, hashing a file named ``SOI_2x1MMI.gds`` in the "components" directory would look like:

.. **Windows**
   - Go to the "components" directory 
   - Right-Click within the folder, "Open in Terminal". Alternatively, run Command Prompt and change your directory to the "components" directory through command line
   - Run ``CertUtil -hashfile SOI_2x1MMI.gds SHA1``. You can select and copy the key by Ctrl+C.
.. **Linux**
   - Open the "components" directory in the terminal
   - ``sha1sum SOI_2x1MMI.gds`` will produce the key, which can be copied (at least in the common distros)
.. **Mac**
   - Move to the component directory in the terminal
  - ``shasum SOI_2x1MMI.gds`` would produce the key to be copied.
.. **Online**
  - Couple of online services for file SHA-1 hashing exist, e.g. <https://emn178.github.io/online-tools/sha1_checksum.html>

.. Assuming the key of ``814dc1e6ab6ee9eb9155beabaef168225686093c`` is generated, the new filename would be ``SOI_2x1MMI_814dc1e6ab6ee9eb9155beabaef168225686093c.gds``.

Component YAML  **Example with commentary**
---------------------------------------------
*name*
  Component name, must be identical to the corresponding GDS file name.
*component_type*
  Component type, should be a member of the Wavephotonics component dictionary. **Allowed entries**
*ports*
  Array of structures containing the optical or electrical port information (port name, port type, port centre, orientation, cross section/port width). **Example**
*modes*
  Array of structures containing supported mode information. Can be detailed within ports individually, or as a component-wide mode information. **Example**

Cross-section GDS
------------------
Cross-sections are used by the 

`Allowed cross sections <./wp_format/cross_sections_list.rst>`_ 



