# clean_imdb_dataset.py


# import packages
import pandas as pd
import numpy as np
import seaborn as sns


def dataframe_info(data):
    # shape and data types of the data
    print(f"The shape of the dataframe = {data.shape}")
    print(f"\nThe data types are: \n{data.dtypes}\n")

    # numeric vs. non-numeric data columns
    select_numeric_columns(data)
    select_non_numeric_columns(data)

    # before cleaning missing values
    print(f"The summary statistics before cleaning:\n{data.describe()}\n")
    pct_missing_values(data)
    visualize_missing_values(data)

    # after cleaning missing values
    print(f"\nThe summary statistics after cleaning:\n{(clean_imdb_df(data)).describe()}\n")
    pct_missing_values((clean_imdb_df(data)))


def select_numeric_columns(data):
    numeric_df = data.select_dtypes(include = [np.number])
    numeric_columns = numeric_df.columns.values
    return print(f"The numeric columns in the dataframe are: \n{numeric_columns}")


def select_non_numeric_columns(data):
    non_numeric_df = data.select_dtypes(exclude=[np.number])
    non_numeric_columns = non_numeric_df.columns.values
    return print(f"The numeric columns in the dataframe are: \n{non_numeric_columns}")


def visualize_missing_values(data):
    missing_columns = data.columns
    colors = ['skyblue', 'royalblue']
    heat_map = sns.heatmap(data[missing_columns].isnull(), cmap=sns.color_palette(colors))
    return heat_map


def pct_missing_values(data):
    for column in data.columns:
        pct_missing = np.mean(data[column].isnull())
    return print('{} - {}%'.format(column, round(pct_missing*100)))


def clean_imdb_df(data):
    # drop missing values of rows
    clean_imdb_data = data.dropna(axis=0)

    # cleaning the introduction and produce_year columns
    intro_clean = clean_imdb_data["introduction"].replace("\n", "", regex=True)
    year_clean = clean_imdb_data["produce_year"].replace("I", "", regex=True).replace(" ", "", regex=True)

    # create new clean columns for introduction and year
    clean_imdb_data["intro"] = intro_clean
    clean_imdb_data["year"] = year_clean

    # renamed the columns back to original names with cleaned data
    clean_imdb_data = clean_imdb_data.drop(columns=["introduction", "produce_year"])
    clean_imdb = clean_imdb_data.rename(columns={"intro": "introduction", "year": "produce_year"})
    return clean_imdb


if __name__ == "main":
    IMDB_data = pd.read_csv("../data/raw/imdb_top_1000_lang_en.csv")
    dataframe_info(IMDB_data)
    clean_data = (clean_imdb_df(IMDB_data)).to_csv("../data/processed/imdb_top_1000_clean.csv", index=False)
