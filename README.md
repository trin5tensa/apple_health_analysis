# Plotting Heart Data from an Apple Watch and iPhone
## What is this project?
This project demonstrates the steps needed to get heart data from the iPhone health app and visualize it using pandas, matplotlib and seaborn in jupyter notebooks. A second set of notebooks shows how to merge and visualize external data from a spreadsheet.

It is not a packaged solution. Jupyter notebooks are tools used to explore data. They are not programs with invisible innards that just run and produce output. In any case, the quantity and nature of your input data will be different and you may need or want to use your own choice of [visualizations](https://seaborn.pydata.org/examples/index.html).

It is not stable. Apple's iOS 15.0.2 allows the health file to be exported As far as I know there is no formal API for the file. In the absence of an API Apple are under no obligation to keep the file format constant nor give any warning of changes. In other words everything here may stop working. 

## Who is it for?
Anyone who wants to see an example of how to use data science tools with Apple health data.

It not intended for anyone who wants to learn data science, jupyter notebooks, numpy, pandas, matplotlib, or seaborn.

## Folder structure
As written the notebooks depend on a folder structure which looks like this:
```
<<Your Project Folder>>
    Data
        Raw
        Processed
    heart_health (support utilities written in pure Python)
    Notebooks
        Additional Data Visualizations
        Apple Heart Data Visualization
    Reports
```

## Export iPhone Health Data
- Open the Health app on the iPhone. 
- Touch the profile picture on the top-right corner. 
- Touch `Export All Health Data` at the bottom of the next screen.
- You will be presented with several options to export the file.
- Save the file to a convenient directory where you can unzip it.
- Unzip the export.zip file. This will produce a folder called `apple_health_export`. Inside the folder is a file called `export.xml`. 
- Move the export.xml file to ` <<Your Project Folder>> / Data / Raw`.
- The `apple_health_export` folder has no further value for this procedure and may be deleted.


## Visualizing the iPhone Health App
### Data Sources
#### Automatic
The Apple watch monitors heart rate and records it in the iPhone Apple Health App.
#### Manual
Blood Pressure must be measured with a pressure cuff and manually entered into the iPhone Apple Health App.

### The Notebooks
#### Apple Heart Data Analysis.ipynb
This notebook opens the `export.xml` file, extracts the heart data, and exports a pickled pandas dataset ready for 
use by the plotting functions.
#### Heart Rate Boxenplot.ipynb
This notebook opens the pickled pandas dataset, extracts the heart rate data, and plots the entire dataset. Three charts are produced: boxplot, boxenplot, and combined boxenplot and observation count.
#### Blood Pressure Boxenplot.ipynb
This notebook opens the pickled pandas dataset, extracts the blood pressure data, and plots a combined boxenplot and observation count.

### Boxenplots (also known as letter plots)
These notebooks mostly produce boxenplots. These show the percentiles 50%, 25% and 75%, 12. 5% and 87.5%, 6.25% 
and 93.75%, and so on until the visualization becomes too small to be meaningful.

Here are some helpful resources whihc explain boxenplots running from from easy to detailed: <br />
[stackoverflow.com: how-boxen-plot-is-different-from-box-plot](https://stackoverflow.com/questions/52403381/how-boxen-plot-is-different-from-box-plot/65894078#65894078) <br />
[towards data science](https://towardsdatascience.com/letter-value-plot-the-easy-to-understand-boxplot-for-large-datasets-12d6c1279c97) <br />
[seaborn Docs](https://seaborn.pydata.org/generated/seaborn.boxenplot.html) <br />
[Original paper](https://vita.had.co.nz/papers/letter-value-plot.html) <br />

## Merging External Data
### Data Sources
#### Medications and other external factors
External data is anything that the iPhone Apple Health App cannot handle such as medication dosages or environmental factors which may affect the heart. They need to be recorded in a spreadsheet and merged with the iPhone data.

### The Notebooks
#### External Factors Analysis.ipynb
This notebook opens the `External Factors.csv` file, cleans up the data, and exports a pickled pandas dataset ready 
for merging with the Apple phone dataset .
#### External Factors Merge.ipynb
This notebook merges the external factor dataset with the Apple phone dataset and exports a pickled pandas dataset ready for use by the plotting notebooks.
#### Tablet Boxenplot.ipynb
This notebook opens the pickled pandas dataset, extracts the data from the tablet column as dosage categories, and 
plots a combined boxenplot and observation count. Each individual dose has its own category.
#### Alcohol Boxenplot.ipynb
This notebook opens the pickled pandas dataset, extracts the data from the alcohol column, creates categories based on ranges and plots a combined boxenplot and observation count.