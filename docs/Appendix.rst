Appendix
~~~~~~~~~

Besides the files that are included in the `submission guidelines <./FormattingGuidelines.rst>`_, the PDK folders also contains the files below for the Wavephotonics (WP) validator to function:

- ``process_overview.yaml`` 
- ``drc_rules.lydrc``
- ``materials\*.csv``
- ``floorplans\floorplans.yaml``
- ``CHANGELOG.md``
- ``layerstack.png``
- ``layers.lyp``

Below, we explain the function of these files for the curious and interested.

process_overview.yaml
______________________

This file provides metadata about the fabrication process flow, as well as the functional layers. Let's take a look at `Si_220nm_active/process_overview.yaml <../Si_220nm_active/process_overview.yaml>`_:

.. code-block::yaml

  process_name: Si_220nm_active
  foundry: CORNERSTONE
  description: SOI 220nm active process
  material: SOI
  is_public: true
  gds_type: only_real_gds
  includes_heaters: true
  includes_rf_layers: true
  has_a_no_metals_option: false

Leaving aside the self-explanatory fields, we have: 

*process_name*
  Name of the process platform, must be identical to the name of the containing folder
*material*
  Material platform used within the process, must be listed within the `list of allowed material platforms <./wp_format/materials_list>`_
*gds_type*
  Describes type of components supplied ( black-boxed, full component, black-boxed with real component swap at tapeout). CORNERSTONE will always use ``only_real_gds``.
*includes_..*
  




The Contributors do not need to interact with these files, as they are defined by the CORNERSTONE fabrication process flows. For the curious and interested, please refer to the explanation of these files below:

`Appendix 1 : process_overview.yaml <./examples/Apdx1_process_overview.rst>`_

`Appendix 2 : drc_rules.lydrc <./examples/Apdx2_drc_rules.rst>`_

`Appendix 3 : material format <./examples/Apdx3_materials.rst>`_

`Appendix 4 : floorplans.yaml <./examples/Apdx4_floorplans.rst>`_
