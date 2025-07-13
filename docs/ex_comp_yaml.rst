Code block with the exmaple yaml file

.. code-block:: yaml

   version: "3.9"
   services:
     app:
       image: my-app:latest
       ports:
         - "8080:80"
       environment:
         - ENV=production
     db:
       image: postgres:13
       volumes:
         - db_data:/var/lib/postgresql/data
   volumes:
     db_data:




.. code-block:: yaml

   name: SOI220nm_1310nm_TE_RIB_2x1_MMI
   component_type: MMI1x2
   modes:
     - mode_numbers:
       - 0
       - 0
       polarisation: TE
       wavelength: 1310
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

