# Coronary-Artery-Disease-ML-Research
Comprehensive Analysis of the Impactful Factors and Prevalence Trends of Coronary Heart Disease

This repository contains SOME OF the code and materials for the research project focusing on the correlation of various health attributes with the presence and risk of coronary heart disease (CHD) in individuals. Please keep in mind this is not all of the materials, please reach out to ryka@seas.upenn.edu for the full project description and code, final paper, presentation slides, and trifold/presentation materials.

## Project Overview

### Research Questions Addressed:

1. **Which health attributes have a statistically significant correlation with coronary heart disease (CHD) in individuals?**
   - Attributes like Thalassemia severity, cholesterol, and systolic blood pressure were found to be significant in determining CHD risk or presence.
   - The TenYearCHD attribute showed little correlation with other features, and no conclusions were drawn from it.
   - Glucose levels showed a strong correlation with diabetes, indicating data accuracy.

2. **Has the prevalence of CHD and stroke changed over the years (in US states)?**
   - The rates of both CHD and stroke have decreased across all age groups from 1998 to 2018.

3. **What states have the highest/lowest prevalence of CHD in individuals ages 35 to 64? Are there any correlations to external dietary factors?**
   - States with the highest CHD prevalence: Kentucky, Kansas, and Nebraska.
   - States/districts with the lowest CHD prevalence: Washington DC, Connecticut, and New Jersey.
   - No direct relationships between heart disease and dietary attributes were found, potentially due to self-reported dietary data from "MyFitnessPal."

4. **How effective are different classification methods for predicting CHD?**
   - Various classifiers, including K-nearest neighbor (KNN), decision trees (DT), and support vector machines (SVC), showed high accuracy (~80% or above) in predicting CHD presence.
   - Max accuracy scores:
     - KNN (UCI Data): 86.88% with 8 neighbors
     - SVC (UCI Data): 88.52% with the RBF kernel
     - DT (UCI Data): 85.25% with 10 features
     - KNN (Framingham Data): 83.60% with 18 neighbors
     - SVC (Framingham Data): 83.97% with the poly kernel
     - DT (Framingham Data): 76.94% with 7 features

## Project Paper

The detailed project paper (unpublished version) can be accessed [here](https://docs.google.com/document/d/1S7JLXQFlWxFenU8YQ6aSatAJmVtDrmwGEIX7PfLKgMc/edit?usp=sharing).
