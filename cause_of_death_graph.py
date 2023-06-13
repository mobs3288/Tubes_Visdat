import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper, Legend, LegendItem
from bokeh.palettes import Spectral6
from bokeh.layouts import column, row
from bokeh.models import Select

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
plot = figure(title='Cause of Death', x_axis_label='Year', y_axis_label='Number of Deaths', plot_height=600, plot_width=1000)

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
def update_plot(attr, old, new):
    selected_country1 = country_select1.value
    selected_disease = disease_select.value
    
    # Mengambil daftar negara yang tersedia untuk dipilih di country_select2
    available_countries = [country for country in country_list if country != selected_country1]
    
    # Memperbarui opsi dropdown untuk memilih negara kedua
    country_select2.options = available_countries
    
    # Memeriksa apakah negara yang dipilih di country_select1 juga dipilih di country_select2
    selected_country2 = country_select2.value
    if selected_country2 == selected_country1:
        # Jika ya, atur negara kedua sebagai negara pertama yang tersedia
        selected_country2 = available_countries[0]
        country_select2.value = selected_country2
    
    # Memfilter data sesuai dengan pilihan pengguna
    filtered_data1 = data[(data["Country"] == selected_country1)]
    filtered_data2 = data[(data["Country"] == selected_country2)]
    
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
country_select1 = Select(options=country_list, value=country_list[0], title='Country 1')
country_select1.on_change('value', update_plot)

# Membuat dropdown untuk memilih negara kedua
country_select2 = Select(options=country_list, value=country_list[1], title='Country 2')
country_select2.on_change('value', update_plot)

# Membuat dropdown untuk memilih penyakit
disease_select = Select(options=disease_list, value=disease_list[0], title='Disease')
disease_select.on_change('value', update_plot)

# Menginisialisasi plot dengan nilai awal
update_plot(None, None, None)

# Menyusun layout
layout = column(country_select1, country_select2, disease_select, plot)

# Menambahkan layout ke current document
curdoc().add_root(layout)
