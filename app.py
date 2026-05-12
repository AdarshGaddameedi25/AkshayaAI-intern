from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():

    df = pd.read_csv('processed_tsla.csv')

    
    table_data = df.tail(20).to_html(classes='table table-striped')

    return render_template('index.html', table=table_data)

if __name__ == '__main__':
    app.run(debug=True)