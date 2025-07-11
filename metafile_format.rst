Formatting guidelines for the GDS files and metafiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple metafile format exists within the infividual PDK folders. An explanation of the file formats will be given here, starting with the metafiles required in the submissions. The other metafiles will be explained in the Appendix.

Formatting guidelines for the submission files
==============================================

Component naming convention:
-----------------------------
The component names should be appended by a unique identifier. This identifier will be temporary prior to the approval so we can use a basic hash algorithm such as SHA-1. The resultant hash key can be appended to the component name. 

You can hash the file ``SOI_2x1MMI.gds`` in the "components" directory through:

*Windows*
  - Go to the "components" directory 
  - Right-Click within the folder, "Open in Terminal". Alternatively, run Command Prompt and change your directory to the "components" directory through command line
  - Run ``CertUtil -hashfile SOI_2x1MMI.gds SHA1``. You can select and copy the key by Ctrl+C.
*Linux*
  - Open the "components" directory in the terminal
  - ``sha1sum SOI_2x1MMI.gds`` will produce the key.
*Online*
  - Couple of online services for file SHA-1 hashing exist, e.g. <https://emn178.github.io/online-tools/sha1_checksum.html>
Assuming the key of ``814dc1e6ab6ee9eb9155beabaef168225686093c`` is generated, the new key 


Component YAML
---------------
*name*
  Component name, should be identical to the GDS file name of the corresponding. It's a good practice to keep the naming
