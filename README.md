# Project-Based Learning: Cricket, Food & Mobile Data Analysis

This repository contains three Python data-analysis projects based on Cricket, Food, and Mobile datasets. It includes the complete PowerPoint presentation, source code, datasets, and generated visualizations.

## Repository contents

```text
project-base-learning/
├── batting.py
├── food.py
├── mobile.py
├── create_visualizations.py
├── teams_clean.csv
├── fastfood.csv
├── mobile_sales.xlsx
├── Three full Datasets ML Data Analysis.pptx
├── requirements.txt
├── README.md
└── Visualization/
    ├── cricket_*.png
    ├── food_*.png
    └── mobile_*.png
```

## Requirements

- Python 3.9 or newer
- pandas
- NumPy
- scikit-learn
- openpyxl
- matplotlib

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the analysis

Open this repository folder in VS Code. Run each dataset analysis from the repository root:

```bash
python batting.py
python food.py
python mobile.py
```

Each script prints the results for its ten questions in the terminal. The datasets are read using paths relative to the repository root.

## Generate visualizations

To regenerate the chart images in the `Visualization` folder, run:

```bash
python create_visualizations.py
```

## Dataset notes and limitations

- The Cricket file does not contain bowling overs and runs conceded, so bowling economy rate cannot be calculated. Wickets are inferred from the dismissal text; this is not a complete bowling scorecard.
- The Food file's `salad` field currently contains only the category `Other`, so a Salad-versus-Other comparison cannot be made from this file.
- The Cricket performance and all-rounder scores are exploratory scoring formulas, not official player rankings. The all-rounder calculation based on dismissal text is an approximation.
- The Mobile spreadsheet includes an `R` column whose meaning is not documented in the supplied workbook; the analysis does not assume what it means.
- Results describe the supplied files only and should not be interpreted as complete market or tournament records.

Before making the repository public, check that you have permission to share the datasets and presentation.
