Guide on forking and submitting a pull request to CORNERSTONE Community Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here, we have a visual guide on the submission process flow within CORNERSTONE Community Repository over the web interface of GitHub. 

1- Fork the original Repository
--------------------------------
Go to the `community repository <https://github.com/cornerstone-uos/cornerstone-community>`_ and "fork" it. Forking allows the user to create a clone of a repository under their own GitHub account, allowing the user to build a personal project based on the source code through version releases without directly modifying the source (`see documentation on GitHub Docs <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks>`_ for more details).
.. image:: ../static/ex3/Fork_1.png
   :width: 900px
   :align: center

.. image:: ../static/ex3/Fork_2.png
   :width: 900px
   :align: center

These will create a personal version of the original source, which holds the diff information between the sourced repository and the fork.

.. image:: ../static/ex3/Fork_3.png
   :width: 900px
   :align: center

2- Create the submission files
---------------------------------

For this example submission, we are going to add an educational template kit built on 300nm SiN process. There are three new design files, two of them being standalone cells (``SiN300nm_1550nm_EduKit_DelayLine`` and ``SiN300nm_1550nm_EduKit_GratingCoupler``)  and a composite/derived cell (``SiN300nm_1550nm_EduKit``) that contains these standalone cells, as well as components found in the source repository (such as MMIs, crossings and heaters). All of the GDS files are accompanied by their Component YAMLs.

.. image:: ../static/ex3/SiN300nm_1550nm_EduKit.png
   :width: 900px
   :align: center

In line with the `formatting guidelines <../FormattingGuidelines.rst>`_, we include the author and ancestry information in the template file, and the author information in the standalone cells. For the referenced cells in the original repository, we provide the hash key of the latest original repository commit that contains the referenced files in the exact shape. The hash key (``872839ed66e5b4b024aa70d65cd2f714ac62f273`` in this case) can be copied by accessing the list of commits (visible in the first image, just below ``Create a new fork``) in the original repository and copying from the corresponding entry:

.. image:: ../static/ex3/VersionHash.png
   :width: 900px
   :align: center

.. code-block:: yaml

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
    
  authors:
  - name: Dr Shengqi Yin
    organisation: Cornerstone / ORC
    email: Shengqi.Yin@soton.ac.uk
  - name: Dr Francesco Floris
    organisation: University of Pavia
    email: francesco.floris@unipv.it

3- Upload the files and push to the fork
-----------------------------------------
To upload the files through the browser in GitHub, go to the relevant folder (``SiN_300nm/components`` in this case) and select `Upload files` from the `Add files` menu. As GitHub Web UI only allows uploads to a single folder at a time, you will need to upload new cross-sections (if they exist) over multiple commits - if you are using Git in your computer, then these can be done in a single commit.

.. image:: ../static/ex3/Upload_1.png
   :width: 900px
   :align: center

After the upload, you can specify the commit details for your benefit. Subsequently, you can commit directly to your fork's ``main``.As there is a pull request template in the Community Repository, the second option will unnecessarily invoke the PR template within your fork. If you are concerned with tidiness of your ``main``, you should create a new branch from the fork ``main`` and commit directly to that branch.

.. image:: ../static/ex3/Upload_2.png
   :width: 900px
   :align: center

Your fork will look similar to the one below following the commit and push:

.. image:: ../static/ex3/Push_to_fork.png
   :width: 900px
   :align: center

4- Create a pull request to the Community Repository

After you uploaded all the new/modified files and would like to make a submission, select ``Open pull request`` from ``Contribute``. It is a good idea to sync to the latest version of the Community Repository from ``Sync fork`` and change the referred commit hash keys in the derived/modified components.

.. image:: ../static/ex3/PullRequest_1.png
   :width: 900px
   :align: center

This will create a pull request template with a Markdown-format commit message for the contributor to modify and fill.

.. code-block:: markdown
    ## Description

  Please include a list of changed components, changed cross-sections, new components and new cross-sections.

  (Optional) If you are submitting in response to an issue, please specify the issue number in the comments.

  ## Type of change

  Please delete options that are not relevant.

  - [x] New component/cross-section 

  ## User verification

  Please specify if you have passed  

  - [x] Platform-specific DRC scripts
  - [ ] (Optional) WP Validator

  ## Screenshots (if applicable)

  You can include any relevant screenshots or recordings here.

  ## Checklist
  - [x] I have read the [Formatting Guidelines](https://github.com/cornerstone-uos/cornerstone-community/blob/main/docs/FormattingGuidelines.rst) and implemented changes accordingly.
  - [x] I have included numerical results, experimental data, manual/documentation and/or an open-access publication DOI where such supplementary information can be accessed by the Community with my submission.
  - [x] I agree to the license conditions specified by TAPR OHL as laid out in [LICENSE.TXT](https://github.com/cornerstone-uos/cornerstone-community/blob/main/LICENSE.txt). 
  - [x] I agree to the terms of [Linux Developer Certificate of Origin (DCO)](https://developercertificate.org/) and especially:
  - [x] I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.
  - [x] I understand that CORNERSTONE preserves the rights to refuse or cease hosting designs that require an export license or have dual-use purpose in the Community repository, subject to annual review and/or government guidance and updates on export control and dual-use technology.
  - [x] I understand the submitted designs can be archived in an open-source format following pre-release acceptance in the Community repository if the functionality of the design cannot be confirmed up to a sensible standard in the fabrication runs. 

  ## Contact

  Contact [PDK Team](mailto:pdk.cornerstone@soton.ac.uk) if you have further questions regarding the pull request.

You can preview the commit message (see below) from the ``Preview`` button above the edit box:

.. image:: ../static/ex3/PullRequest_2.png
   :width: 900px
   :align: center

Click ``Create pull request`` to start the review process by the CORNERSTONE PDK Team.
