Formatting guidelines for the GDS files and metafiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple metafile format exists within the infividual PDK folders. An explanation of the file formats will be given here, starting with the metafiles required in the submissions. The other metafiles will be explained in the Appendix.

Formatting guidelines for the submission files
==============================================
The submitted components must obey to the fabrication process detailed within the Design Guidelines for the specific platform. These details can also be found within the metafiles inside the platform folder, especially in ``process_overview.yaml``, ``drc_rules.lydrc``, ``materials\*.csv``, ``floorplans\floorplans.yaml``. 

Component naming convention:
-----------------------------
The component names should be appended by a unique identifier. This identifier will be temporary prior to the approval so we can use a basic hash algorithm such as SHA-1. The resultant hash key can be appended to the component name. As an example, hashing a file named ``SOI_2x1MMI.gds`` in the "components" directory would look like:

*Windows*
  - Go to the "components" directory 
  - Right-Click within the folder, "Open in Terminal". Alternatively, run Command Prompt and change your directory to the "components" directory through command line
  - Run ``CertUtil -hashfile SOI_2x1MMI.gds SHA1``. You can select and copy the key by Ctrl+C.
*Linux*
  - Open the "components" directory in the terminal
  - ``sha1sum SOI_2x1MMI.gds`` will produce the key, which can be copied (at least in the common distros)
*Mac*
  - Move to the component directory in the terminal
  - ``shasum SOI_2x1MMI.gds`` would produce the key to be copied.
*Online*
  - Couple of online services for file SHA-1 hashing exist, e.g. <https://emn178.github.io/online-tools/sha1_checksum.html>
Assuming the key of ``814dc1e6ab6ee9eb9155beabaef168225686093c`` is generated, the new filename would be ``SOI_2x1MMI_814dc1e6ab6ee9eb9155beabaef168225686093c.gds``.

Component YAML  *Example with commentary*
---------------
*name*
  Component name, must be identical to the corresponding GDS file name.
*component_type*
  Component type, should be a member of the Wavephotonics component dictionary. *Allowed entries*
*ports*
  Array of structures containing the optical or electrical port information (port name, port type, port centre, orientation, cross section/port width). *Example*
*modes*
  Array of structures containing supported mode information. Can be detailed within ports individually, or as a component-wide mode information. *Example*

Cross-section GDS
------------------
Cross-sections are used by the 




