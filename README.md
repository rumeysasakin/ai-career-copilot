# 🔍 AI Kariyer Asistanı — CV & İş İlanı Eşleştirme Sistemi

> Yapay zeka destekli kariyer analiz aracı. CV'nizi bir iş ilanıyla karşılaştırır; eşleşen becerileri, eksikleri ve somut önerileri sunar.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-green.svg)](https://langchain.com)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20(Llama3)-orange.svg)](https://ollama.com)
[![Aşama](https://img.shields.io/badge/Aşama-1%20MVP-yellow.svg)](#proje-yol-haritası)

---

## 📌 Problem

İş arayanlar, bir ilana ne kadar uyduklarını objektif olarak değerlendirmekte zorlanıyor. CV'deki beceriler ile ilandaki gereksinimler arasındaki boşlukları görmek, hangi alanlara yatırım yapılması gerektiğini anlamak zaman alıcı ve subjektif bir süreç.

## 💡 Çözüm

Bu proje, **LangChain** ve **Ollama** kullanarak tamamen yerel çalışan bir yapay zeka asistanı sunar:

- CV metninizi ve iş ilanı metnini giriyorsunuz
- Sistem becerileri çıkarıyor, karşılaştırıyor ve analiz ediyor
- Eşleşen beceriler, eksikler, öneriler ve uyum skoru alıyorsunuz

**Hiçbir API anahtarı veya ücretli servis gerektirmez** — tamamen bilgisayarınızda çalışır.

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

| Araç | Versiyon | Açıklama |
|------|----------|----------|
| Python | 3.11+ | Programlama dili |
| uv | Son sürüm | Paket yöneticisi |
| Ollama | Son sürüm | Yerel LLM çalıştırıcı |

### Kurulum

```bash
# 1. Repoyu klonlayın
git clone https://github.com/rumeysasakin/ai-career-copilot.git
cd ai-career-copilot

# 2. Bağımlılıkları yükleyin
uv sync

# 3. Ollama'dan model indirin (henüz indirmediyseniz)
ollama pull llama3

# 4. Sanal ortamı aktive edin
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 5. Çalıştırın
python main.py
```

### Kullanım

Program başladığında iki seçenek sunulur:

1. **Dosyadan okuma** — Hazır örnek CV ve iş ilanı dosyalarıyla test edin
2. **Elle yapıştırma** — Kendi CV'nizi ve hedeflediğiniz iş ilanını girin

```
============================================================
  🔍 CV - İş İlanı Eşleştirme Sistemi
  LangChain + Ollama ile Beceri Analizi
============================================================

CV metnini nasıl girmek istersiniz?
  1 - Dosyadan oku (ornek_cv.txt)
  2 - Elle yapıştır
Seçiminiz (1/2): 1
✓ CV dosyadan okundu.
```

---

## 📁 Proje Yapısı

```
ai-career-copilot/
├── main.py                 # Ana uygulama — LLM chain ve kullanıcı arayüzü
├── ornek_cv.txt            # Test için örnek CV metni
├── ornek_ilan.txt          # Test için örnek iş ilanı metni
├── pyproject.toml          # Proje yapılandırması ve bağımlılıklar
├── README.md               # Bu dosya
│
├── docs/                   # Dokümantasyon
│   ├── product_perspective.md    # Product Manager perspektifi
│   ├── business_analysis.md      # İş Analisti perspektifi
│   └── technical_architecture.md # AI Engineer perspektifi
│
└── .gitignore
```

---

## ⚙️ Nasıl Çalışır?

```
┌─────────────┐     ┌──────────────────┐     ┌───────────┐     ┌──────────────┐
│  Kullanıcı  │────▶│  PromptTemplate  │────▶│  Ollama   │────▶│   Analiz     │
│  CV + İlan  │     │  (LCEL Chain)    │     │  (Llama3) │     │   Sonucu     │
└─────────────┘     └──────────────────┘     └───────────┘     └──────────────┘
```

1. **Girdi**: Kullanıcı CV metnini ve iş ilanı metnini girer
2. **Prompt**: `PromptTemplate` iki metni yapılandırılmış bir talimata dönüştürür
3. **LLM**: Ollama üzerinden Llama3 modeli metinleri analiz eder
4. **Çıktı**: Eşleşen/eksik beceriler, öneriler ve uyum skoru döner

### Örnek Çıktı

```
## ✅ Eşleşen Beceriler
- Python programlama
- Django framework
- REST API geliştirme
- PostgreSQL veritabanı
- Git versiyon kontrol

## ❌ Eksik Beceriler
- CI/CD süreçleri (GitHub Actions, Jenkins)
- Redis / RabbitMQ
- Kubernetes
- Celery (asenkron görev yönetimi)
- pytest (birim test)

## 💡 Öneriler
- GitHub Actions ile basit bir CI/CD pipeline kurarak portföyünüze ekleyin
- Redis'i öğrenmek için mevcut Django projenize cache ekleyin
- pytest ile mevcut projelerinize test yazarak başlayın

## 📊 Uyum Skoru: %60
```

---

## 🗺️ Proje Yol Haritası

| Aşama | Durum | Açıklama |
|-------|-------|----------|
| **1 — Temel MVP** | ✅ Tamamlandı | CV-ilan karşılaştırma, beceri eşleştirme, öneriler |
| **2 — Agent Yapısı** | 🔜 Sırada | Tool kullanan agent, takip soruları, akıllı kariyer önerileri |
| **3 — Ürünleştirme** | 📋 Planlandı | Streamlit arayüz, PDF yükleme, demo yapılabilir hale getirme |

### Aşama 1 — Temel MVP ✅
- [x] LangChain + Ollama entegrasyonu
- [x] PromptTemplate ile yapılandırılmış analiz
- [x] LCEL chain (pipe operatörü)
- [x] Dosyadan veya elle metin girişi
- [x] Beceri eşleştirme ve eksik analizi
- [x] Uyum skoru hesaplama

### Aşama 2 — Agent ve Akıllı Analiz 🔜
- [ ] LangChain Agent yapısı (tool calling)
- [ ] Beceri çıkarımı için ayrı tool
- [ ] Takip soruları sorabilme (interaktif diyalog)
- [ ] "Hangi projeni öne çıkar" gibi akıllı kariyer önerileri
- [ ] Structured output (JSON formatında çıktı)

### Aşama 3 — Ürünleştirme 📋
- [ ] Streamlit web arayüzü
- [ ] PDF olarak CV yükleme desteği
- [ ] Çoklu ilan karşılaştırma
- [ ] Proje demo videosu
- [ ] Tam dokümantasyon paketi

---

## 📖 Dokümantasyon

Bu projenin farklı perspektiflerden incelenmesi için üç ayrı doküman hazırlanmıştır:

| Doküman | Perspektif | İçerik |
|---------|-----------|--------|
| [Product Perspective](docs/product_perspective.md) | Product Manager | Problem tanımı, kullanıcı segmentleri, değer önerisi, metrikler |
| [Business Analysis](docs/business_analysis.md) | İş Analisti | Gereksinimler, use case'ler, süreç akışları, kabul kriterleri |
| [Technical Architecture](docs/technical_architecture.md) | AI Engineer | Mimari, model seçimi, prompt engineering, teknik kararlar |

---

## 🛠️ Teknoloji Stack

| Teknoloji | Kullanım Amacı |
|-----------|---------------|
| **Python 3.11** | Ana programlama dili |
| **LangChain** | LLM orchestration framework |
| **LangChain LCEL** | Chain yapısı (PromptTemplate \| LLM) |
| **Ollama** | Yerel LLM çalıştırma altyapısı |
| **Llama 3** | Dil modeli |
| **uv** | Paket ve proje yönetimi |

---

## 👩‍💻 Geliştirici

**Rumeysa Sakın**
- Endüstri Mühendisi | Endüstri Mühendisliği Yüksek Lisans Öğrencisi
- Kariyer Odağı: İş Analisti · Product Manager · AI Engineer

---

## 📝 Lisans

Bu proje eğitim ve portföy amaçlı geliştirilmiştir.
