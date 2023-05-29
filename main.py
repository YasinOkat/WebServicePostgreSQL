from flask import Flask, jsonify, request
from datetime import datetime
import psycopg2

app = Flask(__name__)
db_connection_string = "dbname=veritabani user=postgres password=1234 host=localhost"


def get_database_connection():
    conn = psycopg2.connect(db_connection_string)
    cursor = conn.cursor()
    return conn, cursor


@app.route("/", methods=['GET'])
def home():
    return "Merhaba."


@app.route('/login', methods=['POST'])
def login():
    conn, cursor = get_database_connection()

    data = request.get_json()
    kullaniciadi = data.get('kullaniciadi')
    sifre = data.get('sifre')

    query = "SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = %s AND sifre = %s"
    cursor.execute(query, (kullaniciadi, sifre))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    success = result[0] > 0
    return jsonify({'success': success})


@app.route('/getArabalar', methods=['GET'])
def get_arabalar():
    conn, cursor = get_database_connection()

    query = "SELECT plaka FROM arabalar"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    arabalar = [{'Plaka': row[0]} for row in result]
    return jsonify(arabalar)


@app.route('/arabaBirak', methods=['POST'])
def araba_birak():
    conn, cursor = get_database_connection()

    giris_saati_str = datetime.now()
    print(giris_saati_str)

    data = request.get_json()
    kilometre = data.get('kilometre')
    kullanilan_plaka = data.get('plaka')

    query = "UPDATE tbllog SET kilometre = %s, giris_saati = %s WHERE ID = (SELECT ID FROM tbllog WHERE plaka = %s " \
            "ORDER BY ID DESC LIMIT 1)"
    query2 = "DELETE FROM kullanilan_arabalar WHERE kullanilan_plaka = %s"
    query3 = "INSERT INTO arabalar (plaka) VALUES (%s)"

    cursor.execute(query, (kilometre, giris_saati_str, kullanilan_plaka))
    cursor.execute(query2, (kullanilan_plaka,))
    cursor.execute(query3, (kullanilan_plaka,))
    conn.commit()

    cursor.close()
    conn.close()

    if request.content_type != 'application/json':
        return jsonify({'error': 'Request content-type should be application/json'}), 400

    return jsonify({'message': 'success'})


@app.route('/insertData', methods=['POST'])
def insert_data():
    conn, cursor = get_database_connection()

    data = request.get_json()
    plaka = data.get('plaka')
    ad = data.get('ad')
    hedef = data.get('hedef')
    amac = data.get('amac')
    cikis_saati_str = datetime.now()

    query = "INSERT INTO tbllog (cikis_saati, plaka, ad, hedef, amac) VALUES (%s, %s, %s, %s, %s)"
    query2 = "INSERT INTO kullanilan_arabalar (kullanici_adi, kullanilan_plaka, cikis_saati, gidilen_yer) " \
             "VALUES (%s, %s, %s, %s)"

    cursor.execute(query, (cikis_saati_str, plaka, ad, hedef, amac))
    cursor.execute(query2, (ad, plaka, cikis_saati_str, hedef))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'success'})


@app.route('/deleteData', methods=['POST'])
def delete_data():
    try:
        conn, cursor = get_database_connection()

        data = request.get_json()
        plaka = data.get('plaka')
        print('plaka:', plaka)

        query = "DELETE FROM arabalar WHERE plaka = %s"
        cursor.execute(query, (plaka,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'success'})
    except psycopg2.Error as e:
        return jsonify({'error': str(e)})


@app.route('/getKullanilanArabalar', methods=['GET'])
def get_kullanilan_arabalar():
    conn, cursor = get_database_connection()

    query = "SELECT * FROM kullanilan_arabalar"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    kullanilan_arabalar = []
    for row in result:
        kullanilan_arabalar.append({
            'kullanici_adi': row[0],
            'kullanilan_plaka': row[1],
            'cikis_saati': row[2],
            'gidilen_yer': row[3]
        })

    print(kullanilan_arabalar)

    return jsonify(kullanilan_arabalar)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.193')
