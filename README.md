# Plotting Heart Data from an Apple Watch

Plot blood pressure and heart rate recorded on an Apple Watch using pandas, matplotlib and seaborn.

### WARNING
Apple's iOS 15.0.2 allows the health file to be exported. (See below for instructions) As far as I know there is no formal API for the file. In the absence of an API Apple are under no obligation to keep the file format constant nor give any warning of changes. In other words everything here may stop working.

## Health File Preparation
These instructions are correct at 10/27/2010 with iOS 15.0.2.

### Phone Export
Open the Health app on the iPhone. Touch the profile picture on the top-right corner. Touch Export All Health Data at the bottom of the next screen. You will be presented with several options to share the resulting zip file. Save the file to Documents / Coding / Apple Medical / Pandas / Data / Raw

### Prepare for import
On your desktop, unzip the attached archive. Change zip file name to export_YYYY_MM_DD. Change the export.xml file name to export_YYYY_MM_DD.xml and move it to the Raw directory. Discard the unzipped folder and its contents.

Open the notebook, 'Import Phone Data and Preprocess Heart Dataset' and change the import_file_date to YYYY_MM_DD.