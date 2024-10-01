# Import library 
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib

# Class DataAnalyzer untuk analisis data
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    # Fungsi untuk membuat DataFrame yang berisi jumlah pesanan harian dan total revenue
    def create_daily_orders_df(self):
        # Resample data berdasarkan hari menggunakan kolom 'order_approved_at'
        daily_orders_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "order_id": "nunique",  # Menghitung jumlah pesanan unik
            "payment_value": "sum"   # Menjumlahkan total pembayaran (revenue)
        }).reset_index()

        # Mengubah nama kolom agar lebih deskriptif
        daily_orders_df.rename(columns={
            "order_id": "order_count",    # Mengganti 'order_id' menjadi 'order_count'
            "payment_value": "revenue"    # Mengganti 'payment_value' menjadi 'revenue'
        }, inplace=True)
        
        return daily_orders_df
    
    # Fungsi untuk membuat DataFrame total pengeluaran per hari
    def create_sum_spend_df(self):
        # Resample data berdasarkan hari dan menjumlahkan 'payment_value'
        sum_spend_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "payment_value": "sum"   # Menjumlahkan total pembayaran harian
        }).reset_index()

        # Mengubah nama kolom agar lebih mudah dipahami
        sum_spend_df.rename(columns={
            "payment_value": "total_spend"  # Mengganti 'payment_value' menjadi 'total_spend'
        }, inplace=True)

        return sum_spend_df

    # Fungsi untuk membuat DataFrame yang menghitung jumlah item pesanan berdasarkan kategori produk
    def create_sum_order_items_df(self):
        # Group berdasarkan nama kategori produk dan hitung jumlah produk dalam setiap kategori
        sum_order_items_df = self.df.groupby("product_category_name_english")["product_id"].count().reset_index()

        # Mengganti nama kolom agar lebih deskriptif
        sum_order_items_df.rename(columns={
            "product_id": "product_count"  # Mengganti 'product_id' menjadi 'product_count'
        }, inplace=True)

        # Mengurutkan data berdasarkan jumlah produk, dari yang terbanyak
        sum_order_items_df = sum_order_items_df.sort_values(by='product_count', ascending=False)

        return sum_order_items_df

    # Fungsi untuk menghitung skor ulasan dan mengambil skor ulasan yang paling umum
    def review_score_df(self):
        # Menghitung banyaknya setiap skor ulasan
        review_scores = self.df['review_score'].value_counts().sort_values(ascending=False)
        # Mendapatkan skor ulasan yang paling banyak muncul
        most_common_score = review_scores.idxmax()

        return review_scores, most_common_score

    # Fungsi untuk membuat DataFrame jumlah customer per provinsi (state)
    def create_bystate_df(self):
        # Group berdasarkan provinsi dan hitung jumlah customer unik
        bystate_df = self.df.groupby(by="customer_state").customer_id.nunique().reset_index()

        # Mengubah nama kolom
        bystate_df.rename(columns={
            "customer_id": "customer_count"  # Mengganti 'customer_id' menjadi 'customer_count'
        }, inplace=True)

        # Mendapatkan provinsi dengan jumlah customer terbanyak
        most_common_state = bystate_df.loc[bystate_df['customer_count'].idxmax(), 'customer_state']

        # Mengurutkan berdasarkan jumlah customer terbanyak
        bystate_df = bystate_df.sort_values(by='customer_count', ascending=False)

        return bystate_df, most_common_state

    # Fungsi untuk menghitung status pesanan dan status yang paling umum
    def create_order_status(self):
        # Menghitung jumlah setiap status pesanan
        order_status_df = self.df["order_status"].value_counts().sort_values(ascending=False)
        # Mendapatkan status pesanan yang paling umum
        most_common_status = order_status_df.idxmax()

        return order_status_df, most_common_status

# Class BrazilMapPlotter untuk menampilkan peta Brasil dengan overlay data geolokasi
class BrazilMapPlotter:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    # Fungsi untuk menampilkan peta Brasil dan scatter plot geolokasi
    def plot(self):
        # Mengambil gambar peta Brasil dari URL
        brazil_map_url = 'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'
        brazil_image = self.mpimg.imread(self.urllib.request.urlopen(brazil_map_url), 'jpg')

        # Membuat scatter plot dengan data geolokasi
        ax = self.data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10, 10), alpha=0.3, s=0.3, c='maroon')

        # Menampilkan gambar peta Brasil sebagai background
        self.plt.axis('off')  # Mematikan axis karena hanya ingin menampilkan peta
        self.plt.imshow(brazil_image, extent=[-73.98283055, -33.8, -33.75116944, 5.4])  # Atur peta sesuai koordinat Brasil

        # Menampilkan plot di Streamlit
        self.st.pyplot(self.plt)

# Contoh penggunaan:

# Misal kita punya DataFrame `df` yang berisi data pesanan
# df = pd.read_csv('your_dataset.csv')  # Membaca dataset Anda

# Membuat instance dari DataAnalyzer
# analyzer = DataAnalyzer(df)

# Memanggil fungsi yang diinginkan untuk analisis data
# daily_orders = analyzer.create_daily_orders_df()
# by_state, most_common_state = analyzer.create_bystate_df()

# Membuat instance dari BrazilMapPlotter untuk plotting peta
# plotter = BrazilMapPlotter(df, plt, mpimg, urllib, st)
# plotter.plot()  # Menampilkan scatter plot geolokasi di atas peta Brasil
