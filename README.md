# Ames House Price Prediction

Can a home's living area, neighbourhood and year of construction help estimate its sale price? This six-part machine learning project starts with historical sales in Ames, Iowa. The eventual goal is a small app that estimates a sale price in US dollars.

## Part 1 · Understand the dataset

[Open the executed notebook](notebooks/01_understand_the_dataset.ipynb) to see the dimensions, column types and three example sales. Each row represents one residential sale. The target is `price`. The fields `area`, `Neighborhood` and `Year.Built` are examples of information available before a sale.

The data comes from the Ames Assessor's Office and covers 2006–2010. This repository uses OpenIntro's CSV and credits the original study by Dean De Cock. Prices describe that historical market. Applying a future model to current prices or other cities would require new data and evaluation.

[OpenIntro dataset and documentation](https://www.openintro.org/data/index.php?data=ames) · [Original study](https://doi.org/10.1080/10691898.2011.11889627)

## Part 2 · Explore training sales

[Open the analysis and charts](notebooks/02_explore_training_sales.ipynb). We use 2,589 sales from 2006–2009 for exploration and reserve 341 sales from 2010 for final testing. In the training data, the median sale price was **$161,500**. Living area and price had a correlation of **0.709**, with a broad range of prices even for homes of similar size.

## Run the notebooks in VS Code

Install the Python and Jupyter extensions. From a Windows Miniconda prompt, run the following commands.

```shell
git clone https://github.com/shainaulakh/ames-house-price-prediction.git
cd ames-house-price-prediction
conda create -n ames-housing python=3.11 -y
conda activate ames-housing
python -m pip install -r requirements.txt
mkdir data
curl.exe -fL https://www.openintro.org/data/csv/ames.csv -o data/ames.csv
code .
```

If you already have a local clone, open its folder and run `git pull --ff-only` to get the latest files and install the updated requirements in your environment. Open either notebook, choose **Select Kernel → Python Environments → ames-housing**, and select **Run All**. The CSV download needs internet access. Once downloaded, the notebook runs offline. On macOS or Linux, use `curl` in place of `curl.exe`.

## Project progress

- [x] **1. Project setup and dataset** — Load real sales, inspect example records and distinguish features from the target.
- [x] **2. Explore the data** — Reserve test sales and investigate patterns in the training set.
- [ ] **3. Prepare features** — Handle missing values and encode categories inside a reusable pipeline.
- [ ] **4. Compare models** — Compare linear regression with a median-price baseline on validation data.
- [ ] **5. Evaluate predictions** — Investigate errors, finalize the model and report held-out performance.
- [ ] **6. Build and present the app** — Package the pipeline, demonstrate a prediction and document limitations.
