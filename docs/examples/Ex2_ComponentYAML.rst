Example yaml file: ``SiN300nm_1550nm_TE_STRIP_Grating_Coupler_v1p2.yaml``
Tabs will determine the structure order. The comments will be tabbed to make the hierarchy more visible.
This is an example of port-specific modes (instead of a global mode definition)

.. code-block:: yaml

  name: SiN300nm_1550nm_TE_STRIP_Grating_Coupler_v1p2    # A 1550nm TE strip grating coupler for c-band SiN platform
  component_type: GratingCoupler1D                       # A standard TE-mode grating coupler
  ports:                                                 # Ports are being defined
    - center:                                              # Defining the centre of the first port (x=0, y=0)
      - 0.0
      - 0.0
      name: o1                                             # Named o1, optical port, facing -x direction
      orientation: 180                                     
      port_type: optical
      cross_section: strip_1550nm_TE                       # A strip waveguide cross-section
      modes:                                               # The modes are being defined for this port specifically
      - mode_numbers:                                        # Defining mode 1 (the only one here)
        - 0                                                    # It's a TE_00 mode
        - 0
        polarisation: TE                                       # Specifying the polarisation
        wavelength: 1550                                       # C-band design

    - center:                                             # Adding the second port, adding the centre of it
      - 325.81                                              # Centred at (x=325.81, y=0)
      - 0                                                  
      name: vertical_te                                   # Name of the port (can be vertical_te_e1, for example)
      port_type: vertical_te                              # It's a vertical TE mode, common with grating couplers
      orientation: 0.0                                    # It's facing the +x direction
      width:  10.0                                        # It's 10um-wide. For vertical ports, a cross section is not sensible to define
                                                          #   but we will need to define a linear footprint nonetheless
      coupling_angle_cladding: 13.659                     # The injection angle of the free-space beam, defined based on the cladding
                                                          #   The intended fibre angle in the free space is 20 degrees for this design
                                                          #   which sets the NA of the beam to sin(20 degrees)*n_air. The angle in the 
                                                          #   cladding is then arcsin(sin(20 degrees)/n_cladding), which is 13.659 for 
                                                          #   this case. If the design was air-clad, coupling_angle_cladding would have been 20.
      fibre_modes:                                        # The fibre modes defined in this grating coupler.
      - fibre_type: SMF-28                                  # Adding a new mode, for SMF-28 fibre at 1550nm.
        wavelength: 1550                                    # If we had a broadband design for 775nm and 1550nm, for example
                                                            #   then we would have needed another entry here, with a new fibre type and wavelength. 
