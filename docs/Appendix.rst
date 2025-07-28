Appendix
~~~~~~~~~

Besides the files that are included in the `formatting guidelines <./FormattingGuidelines.rst>`_ accompanying the `submission flow <../README.rst#submission-format>`_, the PDK folders also contains the files below for the Wavephotonics (WP) validator to function:

- ``process_overview.yaml`` 
- ``drc_rules.lydrc``
- ``materials\*.csv``
- ``floorplans\floorplans.yaml``
- ``CHANGELOG.md``
- ``layerstack.png``
- ``layers.lyp``

Changes within these files, and components/processes that require such changes will not pass the Submission pre-acceptance checks as they are not compatible with the services provided by CORNERSTONE. 

Below, we explain the function of these files for the curious and interested.

Process overview file (``process_overview.yaml``)
______________________

This file provides metadata about the fabrication process flow, as well as the functional layers. Let's take a look at `SiN_300nm/process_overview.yaml <../SiN_300nm/process_overview.yaml>`_:

.. code-block:: yaml

    process_name: SiN_300nm
    foundry: CORNERSTONE
    description: SiN platform with heaters
    material: SiN
    is_public: true
    gds_type: only_real_gds
    includes_heaters: true
    includes_rf_layers: false
    has_a_no_metals_option: true

Leaving aside the self-explanatory fields, we have: 

*process_name*
  Name of the process platform, must be identical to the name of the containing folder
*material*
  Material platform used within the process, must be listed within the `list of allowed material platforms <./wp_format/materials_list.rst>`_
*gds_type*
  Describes type of components supplied (black-boxed, full component, black-boxed with real component swap at tapeout). CORNERSTONE will always use ``only_real_gds``.
*includes_heaters*, *includes_rf_layers*
  Logical fields for the existence of heaters and RF layers within the platform. 
*has_a_no_metals_option*
  Logical field that specifies if the platform is offered without heater/metal layer for a reduced price. See `Access Charges <https://www.cornerstone.sotonfab.co.uk/mpw-schedule-costs/>`_.

The GDS layer information is then described within ``gds_layers`` field. For each element, we describe the layer information, depth tolerance, DRC rules assigned to the layer, and any aliases to use within the file later on. Practically, the information within the platform design guidelines (see `Design Rules <https://www.cornerstone.sotonfab.co.uk/design-rules/>`_) are described within this section in YAML format.

.. code-block:: yaml

  gds_layers:
    - name: SiN_Etch1_LF_300nm
      layer: [203, 0]
      description: Full SiN etch to BOX (light) for waveguides, layer will be protected. No max feature length @0.35um features.
      drc: 
      - { min_feature_size: 0.25, min_gap: 0.25, max_feature_length: 20.0 }
      - { min_feature_size: 0.35, min_gap: 0.25}
      alias: wg_lf
    - name: SiN_Etch1_DF_300nm
      layer: [204, 0]
      description: Full SiN etch to BOX (dark) for waveguides, layer will be etched. No max feature length @0.35um gaps
      drc: 
      - { min_feature_size: 0.25, min_gap: 0.25, max_feature_length: 20.0 }
      - { min_feature_size: 0.25, min_gap: 0.35}
      alias: wg_df
    - name: Heat_Fil_LF
      layer: [39, 0]
      description: Heater filaments (light), layer will become metal.
      drc: { min_feature_size: 0.6, min_gap: 10.0 }
    - name: Heat_CP_LF
      layer: [41, 0]
      description: Heater contact pads (light), layer will become metal.
      drc: { min_feature_size: 2.0, min_gap: 10.0 }
    - name: Clad_Open_DF
      layer: [22, 0]
      description: Area for oxide etching (dark), layer will be etched. 
      drc: { min_feature_size: 20.0, min_gap: 20.0 }
    - name: Floorplan
      layer: [99, 0]
      is_info_only: true
      description: Cell outline
    - name: Label_Etch_DF
      layer: [100, 0]
      description: Labels (dark), will be etched, will not be checked in DRC
      drc: { min_feature_size: 0.25, min_gap: 0.25 }

Continuing, we have ``layer_stack``, which is designed to assist WP in simulating and exporting the platform components:

.. code-block:: yaml

  layer_stack:
    - name: BOX
      description: BOX - buried oxide
      material: SiO2
      thickness: { value: 3.0 }
      gds_layer: null
    - name: Waveguide
      description: Full thickness SiN layer
      material: SiN
      thickness: { value: 0.3, tol: 0.015 }
      gds_layer: wg_lf or not wg_df
    - name: TOX
      description: Top cladding layer
      material: SiO2
      thickness: { value: 2.0, tol: 0.2 }
      gds_layer: not Clad_Open_DF
    - name: Heater_filament
      description: Heater filament layer (TiN)
      material: metal1
      is_metal_layer: true
      thickness: { value: 0.15, tol: 0.01}
      gds_layer: Heat_Fil_LF
    - name: Contact_pads
      description: Al layer for contact pads and electrical routing
      material: metal2
      is_metal_layer: true
      thickness: { value: 0.22, tol: 0.01}
      gds_layer: Heat_CP_LF

Here, we are using the ``alias`` es described within the ``gds_layers`` to simplify the categorisation of functional regions. As an example, from the desciption of ``TOX`` layer stack, we can see that everywhere on the design file has silicon dioxide as cladding except the regions defined by the ``Clad_Open_DF``, which corresponds to the ``[22/0]`` layer in the GDS files. By defining ``layer_stack`` field, we combine the 2-D information given to us by the GDS file with the depth information, constructing the physical devices for simulations.

DRC file (``drc_rules.lydrc``)
~~~~~~~~~~~~~~~~

This is a file that describes the DRC rules to be performed by KLayout as part of pre-submission design checks. Each platform folder contains a ``drc_rules.lydrc`` file that is identical in the information content to the DRC script provided within `Design Rules <https://www.cornerstone.sotonfab.co.uk/design-rules/>`_.

Material refractive index files (``materials/*.csv``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Material refractive index values across a wavelength range is required for accurate modeling of the components. We provide the refractive index values within a broad spectrum for the materials used in respective platforms in CSV format. These files are located within ``materials`` folder in each platform folder, with file names corresponding to the ``material`` subfield of ``layer_stack`` elements within ``process_overview.yaml`` for the platform.

Floorplans (``floorplans/floorplans.yaml``)
~~~~~~~~~~~~

The ``floorplans`` folder contains the allowed design area specification for the individual platforms in both YAML and GDS formats. These design area specifications can be found within `Access Charges  <https://www.cornerstone.sotonfab.co.uk/mpw-schedule-costs/>`_ or in the Design Guidelines document of the MPW call in `Design Rules <https://www.cornerstone.sotonfab.co.uk/design-rules/>`_.

Layer formatting file (``layers.lyp``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We provide the colour, pattern, border and animation information of the layers to declutter the design window in KLayout. The layer properties follow from the layer numbers and names from the ``gds_layers`` field of the ``process_overview.yaml`` file.

Others
~~~~~~~

We also provide ``layerstack.png`` as a visual representation of the cross-section of the supported waveguides of the platform, and ``CHANGELOG.md`` to keep track of the cumulative changes between consecutive stable release versions of the platforms.

.. image:: ../Si_220nm_active/layerstack.png
   :width: 600px
   :align: center

