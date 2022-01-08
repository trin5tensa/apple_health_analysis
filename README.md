# Plotting Heart Data from an Apple Watch and iPhone

## What is this project?

This project demonstrates the steps needed to get heart data from the iPhone health app and visualize it using pandas, matplotlib and seaborn in jupyter notebooks. A second set of notebooks show how to merge and visualize additional data.

### What isn't this project?
#### A Packaged Solution
Jupyter notebooks are tools used to explore data. They are not programs with invisible innards that just run and 
produce output. In any case, the quantity and nature of your input data will be different and you may need or want to 
use your own choice of [visualizations](https://seaborn.pydata.org/examples/index.html).

#### Reliable
Apple's iOS 15.0.2 allows the health file to be exported As far as I know there is no formal API for the file. In the absence of an API Apple are under no obligation to keep the file format constant nor give any warning of changes. In other words everything here may stop working.

## Who is it for?
Anyone who wants to see an example of how to use data science tools with Apple health data.

### Who isn't it for?
Anyone who wants to learn data science, jupyter notebooks, numpy, pandas, matplotlib, or seaborn.


## Where next?
For instructions on downloading the Apple iPhone health file and running the notebooks see the README.md in the 
folder `/Notebooks/Apple Heart 
Data Visualization`.

For instructions on how to merge external data see the README.md in the folder `/Notebooks/Additional Data 
Visualization`.

### How These Notebooks are Organized
#### Analysis Notebook
The Analysis notebook will usually import raw external data files, clean up the data, and export just the data 
needed for the other notebooks of its folder.
#### Merge Notebook
The optional Merge notebook will merge output from analysis notebooks with other raw data files. It will clean up the data, and export just the data needed for the other notebooks of its folder.
#### Plot Notebooks
Plot notebooks read the intermediate data files produced by the analysis or merge notebooks and use the data to plot 
visualizations. The visualizations are usually saved as jpg and pdf files.