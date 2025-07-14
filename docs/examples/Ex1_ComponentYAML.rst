Here is an example YAML file for a component, a 1x2 MMI, which has one input and two output ports, all optical.  


First, let's define the name of the file.
.. code-block:: yaml

   name: SOI220nm_1310nm_TE_RIB_2x1_MMI

This should be identical to the GDS file name (without the file extension).
Continuing with the component type,

.. code-block:: yaml

   component_type: MMI1x2                 

``component_type`` is not allowed to be arbitrary within the Wavephotonics' YAML format. The list of allowed components can be found `here<../docs/components_list.rst>`_ . Another requirement from Wavephotonics is explicit specification of the modes going through the ports. 

.. code-block:: yaml

   modes:                                 # The modes at the ports are uniform, hence they are defined before the ports structure
     - mode_numbers:                        # The first mode is defined (a TE mode)
       - 0                                     # (0,0) will be the TE_00 mode
       - 0
       polarisation: TE                     # it has polarisation TE
       wavelength: 1310                     # and is defined at 1310. 

Here, we have defined ``modes``, which has only one mode entry, TE_00 mode at 1310nm wavelength. When defined globally for the component this way, the ``modes`` field will be assigned to all the ports of the component. We move on to defining the ports:

.. code-block:: yaml

   ports:                                 
   - name: o1                               
     port_type: optical                     
     center:                                 
     - 0                                      
     - 0
     orientation: 180                        
     cross_section: rib_1310nm_TE
   - name: o2                                                   
     port_type: optical                        
     center:                                 
     - 123.6
     - 1.52500
     orientation: 0                                        
     cross_section: rib_1310nm_TE         
   - name: o3
     port_type: optical
     center:
     - 123.6
     - -1.525
     orientation: 0
     cross_section: rib_1310nm_TE

Here, we defined the three ports within this MMI. First port ``o1`` is the input port, and is facing the -x direction, hence its ``orientation`` is 180. It has a cross-section ``rib_1310nm_TE``, which will be described in ``*/cross-sections/cross_sections.yaml`` - it will be presented as a cross-section example later on.


