YAML Format Explanation
________________________

YAML is a markup language, similar to JSON or XML. Essentially, it is a representation of a struct, both machine-readable and easy to understand for people.

Tab order is important, as it determines the hirearchy within the struct. Within our PDK platforms, YAMLs are used for passing meta-data across different code blocks, with their fields representing target wavelength, port locations, simulation parameters, fabrication geometry details, process tolerances, and so on. 

Below is an example YAML struct for an `unnamed footballer <https://www.flickr.com/photos/87533340@N00/9775464>`_, filled with information from Wikipedia.

.. code-block:: yaml

  name: Name Surname
  position: forward                 
  clubs:
    - country: France
      - Auxerre
      - Marseilles
      - Montpellier
      - Nimes
    - country: UK                        
      - Leeds Utd                                      
      - Man Utd                  
  spouse:                                 
  - name: Name Surname
    married: 1987
    divorced: 2003
    children: 2
  - name: Name Surname
    married: 2007
    children: 2

Here, ``name``, ``position``, ``clubs`` and ``spouse`` all are fields of this struct. ``name`` and ``position`` are strings or char arrays, while ``clubs`` is a cell array of cells (or list of lists in Python). ``spouse`` is a cell array of structs (or list of dicts), with the possibility of having different structs - the first ``spouse`` has a ``divorced`` field, whereas the second one doesn't. If the ``divorced`` field is mandatory during the parsing of this structure, it will throw an error. 

When in doubt, use a parsing tool in your favourite language to see how your YAML file will be processed.

  
