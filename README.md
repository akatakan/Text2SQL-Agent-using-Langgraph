# SQL Sorgulama Asistanı 🤖

Bu proje, doğal dil sorguları kullanarak SQL sorgularını otomatik olarak oluşturan ve veritabanında çalıştıran bir asistan uygulamasıdır.

## 🌟 Özellikler

- Doğal dil sorguları SQL'e dönüştürme
- Otomatik SQL sorgu optimizasyonu ve doğrulama
- Etkileşimli Streamlit arayüzü
- Çoklu LLM desteği (Ollama ve OpenAI)
- Otomatik veri görselleştirme
- Akıllı hata düzeltme ve geri bildirim

## 🛠️ Kurulum

### Yerel Kurulum

1. Projeyi klonlayın:
```bash
git clone [repo-url]
cd [repo-directory]
```

2. Sanal ortam oluşturun ve etkinleştirin:
```bash
python -m venv .venv
# Windows için:
.\.venv\Scripts\activate
# Linux/Mac için:
source .venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env` dosyasını yapılandırın:
```env
DATABASE_URL="sqlite:///[path]/salaries.db"
LLM_MODEL="llama3.1:latest"
LLM_TEMPERATURE=0.1
USE_OLLAMA=true
USE_OPENAI=false
```

### Docker ile Kurulum

1. Docker imajını oluşturun:
```bash
docker build -t sql-assistant .
```

2. Konteyner'ı çalıştırın:
```bash
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  --name sql-assistant \
  sql-assistant
```

## 🚀 Kullanım

### Yerel Kullanım
1. Streamlit uygulamasını başlatın:
```bash
streamlit run app.py
```

2. Tarayıcınızda `http://localhost:8501` adresine gidin
3. Yan menüden LLM ayarlarını yapılandırın
4. Doğal dil ile sorgunuzu yazın ve "Sorguyu Çalıştır" butonuna tıklayın

### Docker ile Kullanım
1. Tarayıcınızda `http://localhost:8501` adresine gidin
2. Yan menüden LLM ayarlarını yapılandırın
3. Doğal dil ile sorgunuzu yazın ve "Sorguyu Çalıştır" butonuna tıklayın

## 📊 Örnek Sorgular

- "Show me the total number of employees for each level"
- "What is the average salary by department?"
- "Show me the highest paid employees in each department"

## 🧪 Testler

Testleri çalıştırmak için:
```bash
pytest tests/
```

## 🏗️ Proje Yapısı

```
.
├── src/
│   ├── analysis/        # Analiz ve mantıksal işlemler
│   ├── core/           # Temel modeller ve konfigürasyon
│   ├── database/       # Veritabanı işlemleri
│   ├── sql/           # SQL işlemleri
│   └── utils/         # Yardımcı fonksiyonlar
├── tests/             # Test dosyaları
├── app.py            # Streamlit arayüzü
├── Dockerfile        # Docker yapılandırması
└── requirements.txt  # Bağımlılıklar
```

## 🔧 Teknik Detaylar

- **LangChain**: LLM entegrasyonu için
- **Streamlit**: Web arayüzü için
- **SQLAlchemy**: Veritabanı işlemleri için
- **Pandas**: Veri manipülasyonu için
- **Pytest**: Test otomasyonu için
- **Docker**: Konteynerizasyon için

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 