# Plotting Heart Data from an Apple Watch and iPhone

Plot blood pressure and heart rate using pandas, matplotlib and seaborn. 

#### Heart rate
If you have an Apple Watch connected to your phone heart rate is measured automatically by the watch and added to 
Apple health records on the phone. 

#### Blood pressure
You will need to take your blood pressure using a manually operated pressure cuff and enter into the health app. Apple do have a patent on a watch band that can measure blood pressure so it may become automatic one day.

#### UTC - In case it matters.
If you see data for a day when you know for sure no data was entered read on. Apple stores times as UTC ± local 
difference so 11 p.m New York on December 25th ends up looking something like "2020-12-26 04:00:00 -05:00:00'. For 
the sake of simplicity local times are ignored and datestamps always show UTC - in this case "2020-12-26 04:00:00".

### WARNING
Apple's iOS 15.0.2 allows the health file to be exported. (See below for instructions) As far as I know there is no formal API for the file. In the absence of an API Apple are under no obligation to keep the file format constant nor give any warning of changes. In other words everything here may stop working.

## Health File Preparation
The following instructions are correct at 12/18/2021 with iOS 15.2 and Watch OS 8.3.

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
- Save the file to a convenient location where you can unzip it.


### Prepare for import
- Unzip the export.zip file. This will produce a folder called `apple_health_export`. Inside the folder is a file called `export.xml`. 
- Move export.xml to ` <Your Project Folder> / Data / Raw`.
- The `apple_health_export` folder has no further value for this procedure and may be trashed.
- Open the notebook, 'Import Phone Data and Preprocess Heart Dataset' and change the import_file_date to YYYY_MM_DD.

Run the Import Phone Data and Preprocess Heart Dataset.ipynb notebook to process the file and produce a pickled 
python file. For me this reduced a half gigabyte xml file to a 5Mb python pickle file. It takes a while.

Next run the Heart Rate Boxenplot.ipynb and Blood Pressure Boxenplot.ipynb notebooks to visualize those datasets. The 
plots will also be saved to the Reports folder as jpg and pdf files.

### Boxenplots (also known as letter plots)

These notebooks produce boxenplots because of the very large datasets. These show the percentiles 50%, 25% and 75%, 12.
5% and 87.5%, 6.25% and 93.75%, and so on until the visualization becomes too small to be meaningful.

Resources on boxenplots from easy to detailed: <br />
[stackoverflow.com: how-boxen-plot-is-different-from-box-plot](https://stackoverflow.com/questions/52403381/how-boxen-plot-is-different-from-box-plot/65894078#65894078) <br />
[towards data science](https://towardsdatascience.com/letter-value-plot-the-easy-to-understand-boxplot-for-large-datasets-12d6c1279c97) <br />
[Original paper](https://vita.had.co.nz/papers/letter-value-plot.html) <br />
[seaborn.docs](https://seaborn.pydata.org/generated/seaborn.boxenplot.html) <br />

