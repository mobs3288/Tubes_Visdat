import streamlit as st
from bokeh.models import Select, RangeSlider
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper, Legend
from bokeh.palettes import Spectral6
from bokeh.embed import file_html
from bokeh.resources import CDN
import pandas as pd

# Set Streamlit title and page config
st.set_page_config(page_title="TUGAS BESAR VISUALISASI DATA")

# Set author names
author_names = "Ryan Oktaviandi Susilo Wibowo(1301204289) and Muhammad Khalid Habiburahman (1301204437)"

# Add title and author names
st.title("TUGAS BESAR VISUALISASI DATA")
st.markdown(f"<div style='text-align: left;'>{author_names}</div>", unsafe_allow_html=True)

# Add small text
st.markdown("IF-43-PIL-DS02")

# Membaca data
data = pd.read_csv("cause_of_deaths.csv")

# Mendapatkan daftar negara, penyakit, dan tahun unik
country_list = data["Country"].unique().tolist()
disease_list = data.columns[3:].tolist()
year_list = data["Year"].unique().tolist()

# Membuat color mapper
color_mapper = CategoricalColorMapper(palette=Spectral6, factors=disease_list)

# Membuat ColumnDataSource awal
source = ColumnDataSource(data={
    'x': [],
    'y': [],
    'disease': [],
    'year': [],
    'country': [],
    'x2': [],
    'y2': [],
    'country2': []
})

# Membuat plot awal
plot = figure(title='Cause of Death', x_axis_label='Year', y_axis_label='Number of Deaths')

# Membuat glyph Circle untuk negara pertama
circle1 = plot.circle(x='x', y='y', source=source, fill_alpha=0.8, size=8, color='blue')

# Membuat glyph Circle untuk negara kedua
circle2 = plot.circle(x='x2', y='y2', source=source, fill_alpha=0.8, size=8, color='red')

# Membuat legend di luar plot
legend = Legend(items=[], location="top_right")
plot.add_layout(legend, 'right')

# Membuat tooltips untuk HoverTool
hover_tool = HoverTool(tooltips=[('Country', ''), ('Year', ''), ('Number of Deaths', '')])

# Menambahkan kondisi untuk tooltips
hover_tool.renderers = [circle1, circle2]
hover_tool.point_policy = 'snap_to_data'

# Membuat tooltips khusus untuk setiap negara
circle1_hover_tool = HoverTool(renderers=[circle1], tooltips=[('Country', '@country'), ('Year', '@year'), ('Number of Deaths', '@y')])
circle2_hover_tool = HoverTool(renderers=[circle2], tooltips=[('Country', '@country2'), ('Year', '@year'), ('Number of Deaths', '@y2')])

# Menambahkan tooltips khusus ke plot
plot.add_tools(hover_tool, circle1_hover_tool, circle2_hover_tool)

# Mengupdate ColumnDataSource dan plot saat nilai dropdown berubah
@st.cache
def update_plot(selected_country1, selected_country2, selected_disease, year_range):
    selected_country1 = str(selected_country1)
    selected_country2 = str(selected_country2)
    start_year, end_year = year_range
    
    # Memfilter data sesuai dengan pilihan pengguna
    filtered_data1 = data[(data["Country"] == selected_country1) & (data["Year"] >= start_year) & (data["Year"] <= end_year)]
    filtered_data2 = data[(data["Country"] == selected_country2) & (data["Year"] >= start_year) & (data["Year"] <= end_year)]
    
    # Mengurutkan data berdasarkan tahun
    filtered_data1 = filtered_data1.sort_values(by='Year')
    filtered_data2 = filtered_data2.sort_values(by='Year')
    
    # Memperbarui data pada ColumnDataSource
    source.data = {
        'x': filtered_data1["Year"],
        'y': filtered_data1[selected_disease],
        'disease': [selected_disease] * len(filtered_data1),
        'year': filtered_data1["Year"],
        'country': [selected_country1] * len(filtered_data1),
        'x2': filtered_data2["Year"],
        'y2': filtered_data2[selected_disease],
        'country2': [selected_country2] * len(filtered_data2)
    }
    
    # Memperbarui label pada sumbu x dan y
    plot.xaxis.axis_label = 'Year'
    plot.yaxis.axis_label = 'Number of Deaths'
    
    # Memperbarui judul plot
    plot.title.text = f"Cause of Death by {selected_disease} Comparison: {selected_country1} vs {selected_country2}"
    
    # Menghapus legend sebelum menambahkan yang baru
    plot.renderers = [r for r in plot.renderers if not isinstance(r, Legend)]
    
    # Membuat legend baru
    legend.items = [(selected_country1, [circle1]), (selected_country2, [circle2])]
    plot.add_layout(legend)

# Membuat dropdown untuk memilih negara pertama
country_select1 = st.selectbox('Country 1', country_list, index=0)

# Mengambil daftar negara yang tersedia untuk dipilih di country_select2
available_countries = [country for country in country_list if country != country_select1]

# Membuat dropdown untuk memilih negara kedua
country_select2 = st.selectbox('Country 2', available_countries, index=1)

# Membuat dropdown untuk memilih penyakit
disease_select = st.selectbox('Disease', disease_list, index=0)

# Membuat slider untuk memilih tahun
year_range = st.slider('Year Range', min_value=min(year_list), max_value=2019, value=(min(year_list), 2019))

# Menginisialisasi plot dengan nilai awal
update_plot(country_select1, country_select2, disease_select, year_range)

# Mengupdate plot saat nilai dropdown atau slider berubah
if st.button('Update Plot'):
    update_plot(country_select1, country_select2, disease_select, year_range)

# Mengubah plot menjadi file HTML
html = file_html(plot, CDN, "Cause of Death Plot")

# Menampilkan plot menggunakan komponen HTML
st.components.v1.html(html, width=1200, height=1000)
