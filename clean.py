import sqlite3

import os
 
# Projendeki veritabanı dosyasının adı (Genellikle realestate.db, database.db veya app.db olur)

# Eğer tam adını biliyorsan aşağıya onu yazabilirsin.

db_adi = "real_estate.db"
 
if os.path.exists(db_adi):

    try:

        conn = sqlite3.connect(db_adi)

        cursor = conn.cursor()
 
        # Mevcut tüm tabloların isimlerini çekiyoruz

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        tablolar = cursor.fetchall()
 
        # Tüm tabloların içini boşaltıyoruz

        for tablo in tablolar:

            if tablo[0] != "sqlite_sequence":

                cursor.execute(f"DELETE FROM {tablo[0]};")

                print(f"🧹 {tablo[0]} tablosu temizlendi.")
 
        conn.commit()

        conn.close()

        print("\n✅ Veritabanındaki tüm veriler başarıyla sıfırlandı!")

    except Exception as e:

        print(f"❌ Bir hata oluştu: {e}")

else:

    print(f"❓ '{db_adi}' adında bir veritabanı dosyası bulunamadı. Lütfen dosya adını kontrol edin.")
 