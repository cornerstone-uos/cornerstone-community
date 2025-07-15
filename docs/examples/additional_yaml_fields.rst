Open-source metadata in the Component YAML files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As part of the submission, we require the Contributors to specify two additional fields within the Component YAMLs:

.. code-block:: yaml
  
  description: Component description
  ancestors:
  - name: Ancestor_Component_Name_1
    commit: HashKey_of_SourceCommit
    modifications: none
  - name: Ancestor_Component_Just_Included
    commit: ReferenceWithinCommit
    modifications: Any sort of modifications
  authors:
  - name: Name Surname or Alias
    organisation: Organisation Formal Name, is Optional
    email: Contributor Email

The ``description`` field explains the functionality and operation principle of the component. 
  
An ``ancestor`` is the closest relative(s) of the contributed Component, i. e. the building blocks the Component is directly based off of. A component might have multiple ancestors or it can have none; it can also have ancestors as part of the same Contributor Submission. ``modifications`` can be ``none`` (the ancestor might have been used directly/translated/rotated), or can include modifications where the component shape was not preserved. We expect the Contributors to define the ``ancestor`` s in the most direct, plain way.

``authors`` are practically the Contributors and any other people who can claim design credits about the component. While the ``organisation`` field is optional, an ``email`` field is required for communication purposes. If the Contributors desire to do so, they can specify an alias (like a GitHub user name) as the ``name`` field.
  
Below is an example, a standalone light detector within ``Si_220nm_active`` platform that is built with a grating coupler and a defect detector (`SOI220nm_1150nm_TE_Defect_Detector <../../Si_220nm_active/components/SOI220nm_1150nm_TE_Defect_Detector.yaml>`_)

.. code-block:: yaml

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

Here, we see that the ``SOI220nm_1550nm_TE_Defect_Detector`` is built on ``SOI220nm_1550nm_TE_IsolatedDetector`` and ``SOI220nm_1550nm_TE_RIB_Grating_Coupler``. As these ancestors are submitted within the same commit as ``SOI220nm_1550nm_TE_Defect_Detector``, the ``commit`` field for both ancestors were set to ``ReferenceWithinCommit``. The ancestors were incorporated directly without modification, hence the ``modification`` fields are set to ``none``.

We require the inclusion of the ancestor information and author information as it is dictated by our license. By tracking the ancestors across commits, we satisfy the Contributor responsibility to provide before/after versions of the "documentation" files (GDS and metafiles), as well as the modification changes. 
