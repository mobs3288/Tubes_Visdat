import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Membaca data
    data = pd.read_csv("cause_of_deaths.csv")

    # Mendapatkan daftar negara, penyakit, dan tahun unik
    country_list = data["Country"].unique().tolist()
    disease_list = data.columns[3:].tolist()
    year_list = data["Year"].unique().tolist()

    # Membuat ColumnDataSource awal
    source = {
        'x': [],
        'y': [],
        'disease': [],
        'year': [],
        'country': [],
        'x2': [],
        'y2': [],
        'country2': []
    }

    # Memperbarui data pada ColumnDataSource
    def update_source(selected_country1, selected_country2, selected_disease):
        filtered_data1 = data[data["Country"] == selected_country1]
        filtered_data2 = data[data["Country"] == selected_country2]
        source['x'] = filtered_data1["Year"].tolist()
        source['y'] = filtered_data1[selected_disease].tolist()
        source['disease'] = [selected_disease] * len(filtered_data1)
        source['year'] = filtered_data1["Year"].tolist()
        source['country'] = [selected_country1] * len(filtered_data1)
        source['x2'] = filtered_data2["Year"].tolist()
        source['y2'] = filtered_data2[selected_disease].tolist()
        source['country2'] = [selected_country2] * len(filtered_data2)

    # Menginisialisasi plot dengan nilai awal
    selected_country1 = country_list[0]
    selected_country2 = country_list[1]
    selected_disease = disease_list[0]
    update_source(selected_country1, selected_country2, selected_disease)

    # Membuat plot awal
    plot = figure(title='Cause of Death', x_axis_label='Year', y_axis_label='Number of Deaths',
                  plot_height=600, plot_width=1000)

    # Membuat glyph Circle untuk negara pertama
    circle1 = plot.circle(x='x', y='y', source=source, fill_alpha=0.8, size=8, color='blue')

    # Membuat glyph Circle untuk negara kedua
    circle2 = plot.circle(x='x2', y='y2', source=source, fill_alpha=0.8, size=8, color='red')

    # Mengupdate ColumnDataSource dan plot saat nilai dropdown berubah
    def update_plot(attr, old, new):
        selected_country1 = country_select1.value
        selected_country2 = country_select2.value
        selected_disease = disease_select.value
        update_source(selected_country1, selected_country2, selected_disease)

    # Menyusun layout
    layout = row(widgetbox(country_select1, country_select2, disease_select), plot)

    script, div = components(layout)

    return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
    app.run()
