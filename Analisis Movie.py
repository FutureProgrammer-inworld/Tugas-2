from flask import Flask, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import ast

app = Flask(__name__)

# Load dataset
df = pd.read_csv("IMBD.csv")

# --- Pembersihan Data dengan Penanganan Null ---

# Kolom 'year'
df['year'] = df['year'].astype(str).str.extract(r'(\d{4})')  # ambil 4 digit angka
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['year'] = df['year'].fillna(0).astype(int)  # isi dengan 0 jika null

# Kolom 'genre'
df['genre'] = df['genre'].fillna('Unknown')
df['genre'] = df['genre'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else 'Unknown')

# Kolom 'rating'
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Imputasi rating null dengan rata-rata rating per genre
rating_mean_per_genre = df.groupby('genre')['rating'].transform('mean')
df['rating'] = df['rating'].fillna(rating_mean_per_genre)
df['rating'] = df['rating'].fillna(0.0)  # jika masih ada null (genre unknown), isi 0.0

# --- Endpoint ---

@app.route("/")
def home():
    return """
    <html>
    <head><title>API Analisis Film</title></head>
    <body>
    <h2>API Analisis Film</h2>
    <p>Gunakan endpoint berikut:</p>
    <ul>
        <li><a href='/genre-populer'>/genre-populer</a></li>
        <li><a href='/rata-rating-genre'>/rata-rating-genre</a></li>
        <li><a href='/grafik-tren-film'>/grafik-tren-film</a></li>
    </ul>
    </body>
    </html>
"""

@app.route("/genre-populer")
def genre_populer():
    populer = df['genre'].explode().value_counts().head(3)
    hasil = populer  
    html = "<h2>3 Genre Paling Populer</h2><ul>"
    for genre, jumlah in hasil.items():
        html += f"<li><b>{genre}</b>: {jumlah} film</li>"
    html += "</ul>"
    return html

@app.route("/rata-rating-genre")
def rata_rating_genre():
    rating_per_genre = df.explode('genre').groupby("genre")["rating"].mean().sort_values(ascending=False)
    html = "<h2>Rata-Rata Rating per Genre</h2><ul>"
    for genre, rating in rating_per_genre.items():
        html += f"<li><b>{genre}</b>: {round(rating, 2)}</li>" # angka 2 di sini arti membulatkan nilai rating menjadi 2 angka. contoh 7.35 jadi 7.3
    html += "</il>"
    return html

@app.route("/grafik-tren-film")
def grafik_tren():
    plt.figure(figsize=(10,5))
    sns.countplot(x="year", data=df[df['year'] >= 2000])
    plt.title("Jumlah Film per Tahun (mulai 2000)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("tren_film.png")
    plt.close()
    return send_file("tren_film.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

