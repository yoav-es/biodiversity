# Biodiversity in U.S. National Parks

This project explores species data from U.S. National Parks to uncover patterns in conservation status, biological categories, and park-level biodiversity. The analysis is performed in a Jupyter Notebook using Python, pandas, and matplotlib. The dataset is inspired by a Codecademy exercise and is based on data from the U.S. National Parks Service.

## Features

- Filters out species with unknown conservation statuses to reveal meaningful trends.
- Identifies biological categories with the highest number of at-risk species.
- Calculates the proportion of at-risk species in each park.
- Maps the distribution of at-risk and recovering species across parks.
- Visualizes key trends in species vulnerability and overall biodiversity.

## Prerequisites

- Python 3.x
- pandas
- matplotlib
- Jupyter Notebook

## Installation

Clone the repository and install the required packages:

```sh
git clone https://github.com/yoav-es/biodiversity.git
cd biodiversity-notebook
pip install pandas matplotlib jupyter
```

## Usage

Launch the Jupyter Notebook to run the analysis step-by-step:

```sh
jupyter notebook biodiversity_analysis.ipynb
```

Follow the notebook cells to explore the data, run the analysis, and view visualizations.

## Files

- **biodiversity_analysis.ipynb** — Main analysis notebook  
- **species_info.csv** — Dataset containing species information  
- **parks_data.csv** — Dataset with park-level species observations  

## Data Source

The dataset is provided by Codecademy and represents fictional data on species in four U.S. National Parks.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.