from flask import Blueprint, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import main3

views = Blueprint('views', __name__)

def load_data(file_path):
    # Replace this with your actual file path
    data_processor = main3.DataProcessing(file_path)
    return data_processor.get_data_frame()

def generate_distribution_plots(df, columns):
    images = []
    std_lst = []
    mean_lst = []
    median_lst = []

    sns.set(style="whitegrid")

    for column in columns:
        plt.figure()
        sns.histplot(df[column], bins=20, kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Density')
        plt.tight_layout()

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        # Encode the plot as base64 for HTML embedding
        img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
        images.append(img_str)

        # Calculate mean and standard deviation
        mean_lst.append(df[column].mean())
        std_lst.append(df[column].std())
        median_lst.append(df[column].median())

    return images, mean_lst, std_lst, median_lst


# Load data once at the beginning
file_path = "./raw_data/data_20231120150040.txt"
df = load_data(file_path)
df.index = range(1, len(df) + 1)

# Define columns of interest
columns_of_interest = ['count', 'minTime', 'maxTime', 'totalTime']

# Generate distribution plots and statistics
images, mean_lst, std_lst, median_lst = generate_distribution_plots(df, columns_of_interest)

@views.route('/')
def home():
    # Pass the first 10 rows of the DataFrame to the template
    return render_template('home.html', table=df.head(10).to_html(classes='table table-striped'))

def render_page_with_statistics(page_number):
    return render_template(
        f'page{page_number}.html',
        image=images[page_number - 1],
        std=std_lst[page_number - 1],
        mean=mean_lst[page_number - 1],
        median=median_lst[page_number-1]
    )

@views.route('/count')
def count():
    return render_page_with_statistics(1)

@views.route('/minTime')
def minTime():
    return render_page_with_statistics(2)

@views.route('/maxTime')
def maxTime():
    return render_page_with_statistics(3)

@views.route('/totalTime')
def totalTime():
    return render_page_with_statistics(4)

@views.route('/wholeData')
def wholeData():
    return render_template('page5.html', table=df.to_html(classes='table table-striped'))
