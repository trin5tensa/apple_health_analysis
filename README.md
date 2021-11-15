# Plotting Heart Data from an Apple Watch

Plot blood pressure and heart rate recorded on an Apple Watch using pandas, matplotlib and seaborn.

### WARNING
Apple's iOS 15.0.2 allows the health file to be exported. (See below for instructions) As far as I know there is no formal API for the file. In the absence of an API Apple are under no obligation to keep the file format constant nor give any warning of changes. In other words everything here may stop working.

## Health File Preparation
The following instructions are correct at 10/27/2021 with iOS 15.0.2.

### File structure
These notebooks assume the following folder structure inside your project folder:

```
Your Project Folder
    Data
        Raw
        Processed
    Notebooks
    Reports
```
### Phone Export
- Open the Health app on the iPhone. 
- Touch the profile picture on the top-right corner. 
- Touch Export All Health Data at the bottom of the next screen.
- You will be presented with several options to export the file. 
- Save the file to a convenient location where you can unzip it and organize the files which will be produced.


### Prepare for import
- Change the name of the exported file from `export.zip` to `export_YYYY_MM_DD.zip`. This will distinguish between future exports.
- Unzip the export.zip file. This will produce a folder called `apple_health_export`. Inside the folder is a file called `export.xml`. 
- Change the name to export_YYYY_MM_DD.xml
- Move export_YYYY_MM_DD.xml to ` <Your Project Folder> / Data / Raw`.
- The `apple_health_export` folder has no further value for this procedure and may be trashed.
- Open the notebook, 'Import Phone Data and Preprocess Heart Dataset' and change the import_file_date to YYYY_MM_DD.

Run the notebook to process the file and produce a pickled python file. For me this reduced a half gigabyte xml file to a 5Mb python pickle file. It takes a while.