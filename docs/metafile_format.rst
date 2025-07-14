Formatting guidelines for the GDS files and metafiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cornerstone collaborates with `Wavephotonics <https://wavephotonics.com>`_ to export its PDKs to EDA libraries. We use the building block verification tools created by Wavephotonics, and require some of the metafiles from the Community Members as part of the submission process.  Multiple metafile format exists within the infividual PDK folders. An explanation of the required files will be given here, and the other metafiles for compliance with Wavephotonics workflow will be explained in the Appendix.

Formatting guidelines for the submission files
==============================================

A minimal submission would include a component GDS file for an individual component, and a YAML metafile accompanying it for the component description. These component files would need to be placed within the ``components`` directory of the platform folder it belongs to (e. g. ``Si_220nm_active/comonents/``).

If the submitted component contains ports that have cross-sections different than the ones defined in ``cross-sections`` folder of the platform (e. g. ``Si_220nm_active/cross-sections/``), then the new cross-section will be required as a GDS file, alongside a new cross-section entry within ``cross-sections/cross_sections.yaml`` metafile.

Beyond these, the Community Members do not need to submit any other files. However, numerical simulations or experimental data submissions in tabular form are welcome, and Members are encouraged to provide them within the component YAMLs as struct fields.

The submitted components must obey to the fabrication process detailed within the Design Guidelines for the specific platform. These details can also be found within the metafiles inside the platform folder, especially in ``process_overview.yaml``, ``drc_rules.lydrc``, ``materials\*.csv``, ``floorplans\floorplans.yaml``.


Component naming convention:
-----------------------------
.. The component names should be appended by a unique identifier. This identifier will be temporary prior to the approval so we can use a basic hash algorithm such as SHA-1. The resultant hash key can be appended to the component name. As an example, hashing a file named ``SOI_2x1MMI.gds`` in the "components" directory would look like:

.. **Windows**
   - Go to the "components" directory 
   - Right-Click within the folder, "Open in Terminal". Alternatively, run Command Prompt and change your directory to the "components" directory through command line
   - Run ``CertUtil -hashfile SOI_2x1MMI.gds SHA1``. You can select and copy the key by Ctrl+C.
**Linux**
   - Open the "components" directory in the terminal
   - ``sha1sum SOI_2x1MMI.gds`` will produce the key, which can be copied (at least in the common distros)
**Mac**
   - Move to the component directory in the terminal
  - ``shasum SOI_2x1MMI.gds`` would produce the key to be copied.
**Online**
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

`Allowed cross sections <./cross_sections_list.rst>`_ 



