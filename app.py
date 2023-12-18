import pickle
import numpy as np
from flask import Flask, url_for, render_template, request

model = pickle.load(open('model/model.pkl','rb')) # [kamar_tidur, LB, LH, BB, BK, BS, BTE, BTI, BU]


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    kecamatan = ['Balikpapan Barat', 'Balikpapan Kota', 'Balikpapan Selatan', 'Balikpapan Tengah', 'Balikpapan Timur', 'Balikpapan Utara']

    kamar_tidur = int(request.form.get('kamar_tidur'))
    luas_bangunan = int(request.form.get('luas_bangunan'))
    luas_lahan = int(request.form.get('luas_lahan'))
    selected_kecamatan = request.form.get('kecamatan')

    daerah = [0] * len(kecamatan)
    daerah[kecamatan.index(selected_kecamatan)] = 1

    feature = [np.array([kamar_tidur, luas_bangunan, luas_lahan] + daerah)]

    hasil = int(model.predict(feature))
    bawah = '{:,.0f}'.format(hasil - 200000000)
    atas = '{:,.0f}'.format(hasil + 200000000)
    o = f'Rp{bawah} - Rp{atas}'

    return render_template('index.html', harga=o)

if __name__ == '__main__':
    app.run(debug=True)