# Advanced submission: Ancestry-related YAML fields

We are going to outline a hypothetical submission based on one of our off-the-shelf designs (`SiN300nm_1550nm_EduKit`). Let's assume there are three new design files, two of them being standalone cells (`SiN300nm_1550nm_EduKit_DelayLine` and `SiN300nm_1550nm_EduKit_GratingCoupler`) and a composite/derived cell (`SiN300nm_1550nm_EduKit`) that contains these standalone cells, as well as components found in the source repository (such as MMIs, crossings and heaters). All of the GDS files are accompanied by their Component YAMLs.

<img src="../_static/SiN300nm_1550nm_EduKit.png" class="align-center" width="600" alt="image" />

## Obtain hash keys for the builing block commits

In line with the [formatting guidelines](../guidelines/Guidelines_Advanced.md), we include the author and ancestry information in the template file, and the author information in the standalone cells. For the referenced cells in the original repository, we provide the hash key of the latest original repository commit that contains the referenced files in the exact shape. The hash key (`872839ed66e5b4b024aa70d65cd2f714ac62f273` in this case) can be copied by accessing the list of commits in the original repository and copying from the corresponding entry:

<img src="../_static/VersionHash.png" class="align-center" width="900" alt="image" />

``` yaml
# Tail of the Component YAML for the template file 
ancestors:
- name: SiN300nm_1550nm_EduKit_DelayLine
  commit: ReferenceWithinCommit
- name: SiN300nm_1550nm_EduKit_GratingCoupler
  commit: ReferenceWithinCommit
- name: SiN300nm_1550nm_TE_STRIP_Crossing
  commit: 872839ed66e5b4b024aa70d65cd2f714ac62f273
- name: SiN300nm_1550nm_TE_STRIP_2x1_MMI
  commit: 872839ed66e5b4b024aa70d65cd2f714ac62f273
- name: SiN300nm_1550nm_TE_STRIP_2x2_MMI
  commit: 872839ed66e5b4b024aa70d65cd2f714ac62f273
- name: Heater
  commit: 872839ed66e5b4b024aa70d65cd2f714ac62f273
```
## Provide credits
Provide credits is up to the contributor. Please note that providing credits does not provide a legal basis to submit a component; please make sure that you have the rights to share/disseminate the component (see [repository licence](../../LICENSE.txt))
``` yaml
authors: # this field is blanked in the example.
- name: github_user
  email: user_mail@mail.example
- name: Name Surname
  organisation: ExampleCompany LLC
  email: surname.name@company.com
```

If you are concerned that you will make a mistake during the submission, you can submit the details of the ancestors and their versions within the pull request template without modifying the YAML files. Having appropriate version information within the submissions prevents dimension mismatches and confusion in tapeout.

