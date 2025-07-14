Here is an example YAML file for a component, a 1x2 MMI, which has one input and two output ports, all optical.  

.. code-block:: yaml
   name: SOI220nm_1310nm_TE_RIB_2x1_MMI
Name of the GDS file
.. code-block:: yaml
   component_type: MMI1x2                 # Select from the list of components
   modes:                                 # The modes at the ports are uniform, hence they are defined before the ports structure
     - mode_numbers:                        # The first mode is defined (a TE mode)
       - 0                                     # (0,0) will be the TE_00 mode
       - 0
       polarisation: TE                     # it has polarisation TE
       wavelength: 1310                     # and is defined at 1310. 
   # If there are more than one mode present - locally or globally, for a new polarisation, mode number, or wavelength, make another entry to the modes.
   ports:                                 # The ports will be defined. This is a 2x1 MMI, and it will have three optical ports with rib cross-sections.
   - name: o1                                # Defining the first port, which is an input port
     port_type: optical                      # Select port type from the list of ports
     center:                                 # The port is centred
     - 0                                        # x=0, y=0
     - 0
     orientation: 180                        # and is oriented 180 degrees - meaning the signal will be injected from -x direction.
     cross_section: rib_1310nm_TE            # and it has "rib_1310nm_TE" cross section, which needs to be defined within the "cross-sections" folder.
   # new port definition
   - name: o2                                # Second port (output)                    
     port_type: optical                      # Optical   
     center:                                 # Centred at x=123.6, y= -1.525
     - 123.6
     - 1.52500
     orientation: 0                          # Oriented at 0 degrees - the signal will be leaving towards +x                
     cross_section: rib_1310nm_TE            # The cross section is defined
   # and the remaining ports are named
   - name: o3
     port_type: optical
     center:
     - 123.6
     - -1.525
     orientation: 0
     cross_section: rib_1310nm_TE
