# How to use "cell_bbox" macro in KLayout?

This macro is useful in instances where the centre-off-mass for multiple selected polygons are to be found (e.g. for gratings).

## Download
To start using this macro, first download the [source file](../references/cell_bbox.lym). This file is a slightly modified version of the macro with the same name in KLayout website ([see original](https://www.klayout.org/svn-public/klayout-resources/trunk/scripts/cell_bbox.lym)) to include the centre-of-mass location in the information window.

## Import into KLayout

Import into KLayout by opening KLayout, then selecting **Macros** from the toolbar. Click on Import File symbol on the upper-left toolbar, then select the downloaded file. Close the Macros tab to see it listed under **Tools-> Cell Bounding Box**

## Open your GDS file 

The macro looks for a selected cell to define the bounding box - if called on an empty KLayout instance it will throw an error. Open your GDS file and copy the desired polygons into a new layout (**File->New Layout** with the default settings, ```Crtl+C```,```Ctrl+V``` work for copy-paste).

## Run macro

From **Tools->Cell Bounding Box**, run the macro to see the centre position of the copied polygons

