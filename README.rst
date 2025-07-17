Cornerstone Community Repository
================================================

.. image:: ../docs/static/CORNERSTONE_Logo_Revised Colours.png
   :width: 200px
   :align: center

Welcome to CORNERSTONE Community repository! 

Aim & Vision
~~~~~~~~~~~~~

Create an environment where community members can:

* Contribute to a public library of components for the benefit of other users
* Hold discussions over improvements on the designs, or alternative methodologies
* Form a library of elements that have accessible metadata for easy integration into custom codes.

Submission format
~~~~~~~~~~~~~~~~~~
We aim to incorporate the Community repository into the Wavephotoncis (WP) PDK Portal. WP has provided guidelines and tests for validation of the components and supporting metafiles. It is expected from the Member to adhere to the WP metafile format, which are outlined in the  `formatting guidelines <./docs/FormattingGuidelines.rst>`_.

To start, fork the repository. This will give you access to all of the Communiy PDK folders. Instructions below are suitable for submission to a single platform. For multi-platform submissions, cycle through the instructions for each platform.

(a) Place the new GDS files for your components, with naming convention ``<Platform>_<Wavelength>_<ComponentName>.gds`` into ``components`` folder of the platform folder.
(b) Create a YAML file for each component. You can base the component YAML on the existing YAMLs of similar components. If a new port cross-section is needed in the YAML, put a placeholder for the new port for now.
(c) Create the GDS file for the new cross section in ``cross-sections`` folder. The GDS file will contain a structure 50um long in x-axis, and has the linear cross section along y-axis. The name of the GDS file will be the name of the cross-section.
(d) Append the new cross-section metadata into the ``cross_sections.yaml`` file within ``cross-sections`` folder.
(e) Within the Component YAMLs, specify your name/alias and email as an author. A component or a file can have more than one author.
(f) Include the ancestry of the component in the Component YAML file. The ancestry should include the prior component(s) that the new component is based on. One level of ancestry is sufficient.

Submission acceptance stages 
~~~~~~~~~~~~~~~~

The initial version is comprised of components that have been previously fabricated and characterised. We aim to make the characterisation results public as soon as possible.

We expect the new component submissions to follow a verification flow:

(i) Community member submits a new design file, either an original file made publicly available by the user, or a modification to an already-existing component within the Community repository.
(ii) The submission will be reviewed by the Cornerstone team for compliancy with the licensing and export policies. If the submission is rejected, a detailed feedback will be provided to the contributor.
(iii) The pre-approved submission will be cross-referenced with the already-existing, NDA-gated libraries to confirm no IP infringement has taken place.
(iv) A pre-release without functionality confirmation will be made available in the repository for the use of the Community as an alpha version.
(v) A test batch will be fabricated alongside confirmed components for characterisation of the new submission.
(vi) Provided the functionality of the components is confirmed, it will be incorporated into the stable version of the Community.
(vii) Components whose functionalities couldn't be verified will be sent back to the contributor alongside experimental data and feedback.

License
~~~~~~~
The Cornerstone Community repository is licensed with `TAPR Open Hardware License <https://tapr.org/the-tapr-open-hardware-license/>`_

Contact
~~~~~~~~

`Contact us <mailto:pdk.cornerstone@soton.ac.uk>`_ for questions related to the your Community submissions, Community repository contents - or any other issues related to the Community repository.






