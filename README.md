CarHub - İkinci El Araç Alım Satım Platformu
CarHub, kullanıcıların güvenle araç ilanı verebildiği, detaylı filtreleme seçenekleriyle hayallerindeki araca ulaştığı ve satıcılarla iletişim kurabildiği modern bir web uygulamasıdır.
***Öne Çıkan Özellikler***
--->Dinamik İlan Listeleme: Veritabanındaki en güncel ilanlar ana sayfada vitrin olarak sergilenir.
--->Gelişmiş Arama & Filtreleme: Marka, model, fiyat aralığı, yakıt türü ve konuma göre anlık filtreleme yapabilen gelişmiş arama motoru.
--->Güvenli Kullanıcı Yönetimi: Kayıt olma, giriş yapma ve profil yönetimi işlemleri şifrelenmiş (hash) şifreleme yöntemiyle korunur.
--->Resim Optimizasyonu: Yüklenen araç fotoğrafları Pillow kütüphanesi ile otomatik olarak yeniden boyutlandırılır ve sunucuda optimize edilerek saklanır.
--->Mesajlaşma Sistemi: Alıcı ve satıcıların ilan üzerinden birbirleriyle iletişime geçebilmesini sağlayan dahili mesaj kutusu.

***Kullanılan Teknolojiler***
""Backend""
Python & Flask: Uygulama mimarisi ve yönlendirmeler.
PostgreSQL: İlişkisel veritabanı yönetimi.
SQLAlchemy: Veritabanı işlemleri için ORM katmanı.
Flask-Login: Oturum yönetimi ve güvenlik.
""Frontend""
HTML5 & CSS3: Sayfa yapısı ve özel tasarımlar.
Bootstrap 5: Duyarlı (responsive) tasarım ve modern arayüz bileşenleri.
Jinja2: Sunucu taraflı şablon motoru.

***Katmanlı Mimari Yapısı***
Routing (Blueprint) Katmanı: Uygulama; auth, listings, messages, user ve main olmak üzere 5 ana modüle ayrılmıştır. Her modül kendi rotalarını ve iş mantığını bağımsız olarak yönetir.
Data Katmanı (Models): models.py içinde tanımlanan SQLAlchemy sınıfları ile PostgreSQL veritabanı şeması yönetilir. migrations/ klasörü ile veritabanı sürümleri takip edilir.
Presentation (Templates) Katmanı: Jinja2 şablon motoru kullanılarak base.html iskeleti üzerinden tüm sayfalar dinamik olarak türetilir.
Business Logic (Search & Utils): Arama algoritmaları search.py içinde, resim işleme ve dosya yönetimi gibi yardımcı fonksiyonlar ise utils.py içinde merkezileştirilmiştir.

***Kurulum ve Çalıştırma***
Depoyu klonlayın:
Bash
git clone https://github.com/HilalEsma-ylmz/car_market.git
cd car_market

Gerekli kütüphaneleri yükleyin:
Bash
pip install -r requirements.txt

Uygulamayı başlatın:
Bash
python run.py
