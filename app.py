import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

from flask import Flask, render_template

# Load the data from the CSV file
df = pd.read_csv('Hydra-Movie-Scrape.csv')

# Create a Flask app instance
app = Flask(__name__)

# Helper function to convert a Matplotlib plot to a base64-encoded PNG image
def plot_to_base64_string(plot):
    buffer = io.BytesIO()
    plot.savefig(buffer, format='png')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

# Define a Flask route to display all three visualizations
@app.route('/')
def index():
    # Generate the first visualization
    plt.subplot(3, 2, 1)
    plt.hist(df['Year'], bins=20, color='skyblue')
    plt.title('Distribution of Movies by Year')
    plt.xlabel('Year')
    plt.ylabel('Frequency')

    # Convert the plot to a base64-encoded PNG image
    plot_base64_1 = plot_to_base64_string(plt)

    # Generate the second visualization
    plt.clf() # clear the current figure
    plt.subplot(3, 2, 2)
    df['Runtime'].plot(kind='density', color='purple')
    plt.title('Density Plot of Movie Runtimes')
    plt.xlabel('Runtime')
    plt.ylabel('Density')

    # Convert the plot to a base64-encoded PNG image
    plot_base64_2 = plot_to_base64_string(plt)

    # Generate the third visualization
    plt.clf() # clear the current figure
    plt.subplot(3, 2, 3)
    genres = df['Genres'].str.split(',', expand=True).stack().str.strip().value_counts()
    genres.plot(kind='bar', color='orange')
    plt.title('Distribution of Movies by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Frequency')

    # Convert the plot to a base64-encoded PNG image
    plot_base64_3 = plot_to_base64_string(plt)

    # Define the HTML content
    html_content = render_template('index.html', plot_base64_1=plot_base64_1, plot_base64_2=plot_base64_2, plot_base64_3=plot_base64_3)

    # Return the HTML content
    return html_content

if __name__ == '__main__':
    app.run(debug=True)
