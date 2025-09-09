# YAML Format Explanation

[YAML](https://en.wikipedia.org/wiki/YAML) is a markup language, similar to JSON or XML. Essentially, it is a representation of a struct, both machine-readable and easy to understand for people.

Tab order is important, as it determines the hirearchy within the struct. Within our PDK platforms, YAMLs are used for passing meta-data across different code blocks, with their fields representing target wavelength, port locations, simulation parameters, fabrication geometry details, process tolerances, and so on.

Below is an example YAML struct that contains information on Si, sourced from Wikipedia.

``` yaml
name: Silicon
symbol: Si              
properties:
- physical:
  - crystal structure: FCC
  - lattice constant: 543.1 pm
  - bandgap: 1.12 eV
  - resistivity: 1300 Ohm*m
  - refractive index at 1550nm : 3.48 
- mechanical: 
  - melting point: 1414 C
  - boiling point: 3265 C
  - Mohs hardness: 6.5
  - Young modulus: 130-188 GPa
  - density: 2.329 g/cm^3
notable compounds:
- name: Silicon dioxide
  uses:
    - fibres
    - glass wool
    - passivation
- name: Silicon carbide
  uses:
    - abrasives
    - power electronics
    - colour centres
- name: Silicates
  uses:
    - ceramics
    - cement
    - jewellery
- name: Silicones
  uses:
    - cookware
    - PDMS
```

Here, `name`, `symbol`, `properties` and `notable compounds` all are fields of this struct. In Python, this struct is imported as a dictionary with the field names corresponding to keys, though it is possible to write a custom parser to accommodate different needs. Lines starting with `-` denote the existence of a list; e.g. `notable compounds` key will return a list, which contains dicts that contain information on `Silicon dioxide`, `Silicon carbide`, `Silicates` and `Silicones`. 

To see how a YAML file loads, you can load and visualise the imported file with
``` 
import yaml
from pprint import pprint

with open('dummyfile.yaml', 'r') as file:
    data = yaml.safe_load(file)

pprint(data)
```
after installing `pyyaml` via `pip install pyyaml`.