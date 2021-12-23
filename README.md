# Plotting Heart Data from an Apple Watch and iPhone


Plot blood pressure and heart rate using pandas, matplotlib and seaborn. 


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
- Save the file to a convenient location where you can unzip it and organize the files which will be produced.


### Prepare for import
- Change the name of the exported file from `export.zip` to `export_YYYY_MM_DD.zip`. This will distinguish between future exports.
- Unzip the export.zip file. This will produce a folder called `apple_health_export`. Inside the folder is a file called `export.xml`. 
- Change the name to export_YYYY_MM_DD.xml
- Move export_YYYY_MM_DD.xml to ` <Your Project Folder> / Data / Raw`.
- The `apple_health_export` folder has no further value for this procedure and may be trashed.
- Open the notebook, 'Import Phone Data and Preprocess Heart Dataset' and change the import_file_date to YYYY_MM_DD.

Run the notebook to process the file and produce a pickled python file. For me this reduced a half gigabyte xml file to a 5Mb python pickle file. It takes a while.

### Boxenplots

The large datasets require a better visualization than that provided by boxplots so seaborn's boxenplots have been used.

Explanations of boxenplots (also known as letter plots): <br />
[towards data science](https://towardsdatascience.com/letter-value-plot-the-easy-to-understand-boxplot-for-large-datasets-12d6c1279c97) <br />
[stackoverflow.com](https://stackoverflow.com/questions/52403381/how-boxen-plot-is-different-from-box-plot) <br />
[Original paper](https://vita.had.co.nz/papers/letter-value-plot.html) <br />
[seaborn.docs](https://seaborn.pydata.org/generated/seaborn.boxenplot.html) <br />

#### Boxenplot stopping criterion
A stopping criterion is used to determine the last letter-value k for which a box should be visualized. For every 
letter-value, the trustworthiness is determined by calculating the 95% confidence interval around it. If the interval overlaps with the previous letter-value, the uncertainty for the current letter-value is too high. In this case, the letter-value and the following values are not displayed anymore.
In seaborn other algorithms are available for stopping criteria.

