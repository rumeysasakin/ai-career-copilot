# 🔍 AI Kariyer Asistanı — CV & İş İlanı Eşleştirme Sistemi

> Yapay zeka destekli kariyer analiz aracı. CV'nizi bir iş ilanıyla karşılaştırır; eşleşen becerileri, eksikleri ve somut önerileri sunar.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-green.svg)](https://langchain.com)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20(Llama3)-orange.svg)](https://ollama.com)
[![Aşama](https://img.shields.io/badge/Aşama-2%20Agent-green.svg)](#proje-yol-haritası)

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

# 3. Ollama'dan modelleri indirin (henüz indirmediyseniz)
ollama pull llama3       # Mod 1 (Chain) için
ollama pull llama3.1     # Mod 2 (Agent) için — tool calling desteği

# 4. Sanal ortamı aktive edin
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 5. Çalıştırın
python main.py
```

### Kullanım

Program başladığında iki mod sunulur:

1. **Basit Analiz (Chain)** — Sabit akışta tek seferde LLM analizi (Llama 3)
2. **Akıllı Analiz (Agent)** — Tool'larla adım adım analiz + kişisel değerlendirme (Llama 3.1)

```
============================================================
  🔍 AI Kariyer Asistanı — CV & İş İlanı Eşleştirme
  LangChain + Ollama ile Beceri Analizi
============================================================

Hangi modu kullanmak istersiniz?
  1 - Basit Analiz (Chain — Aşama 1)
  2 - Akıllı Analiz (Agent — Aşama 2)
Seçiminiz (1/2): 2

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
├── main.py                 # Ana uygulama — mod seçimi, girdi alma, çıktı gösterimi
├── agent.py                # Aşama 2 — Agent yapısı (create_agent + LangGraph)
├── tools.py                # Agent tool'ları (beceri_cikar, karsilastir, skor, öneri)
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

### Mod 1 — Chain (Basit Akış)
```
┌─────────────┐     ┌──────────────────┐     ┌───────────┐     ┌──────────────┐
│  Kullanıcı  │────▶│  PromptTemplate  │────▶│  Ollama   │────▶│   Analiz     │
│  CV + İlan  │     │  (LCEL Chain)    │     │  (Llama3) │     │   Sonucu     │
└─────────────┘     └──────────────────┘     └───────────┘     └──────────────┘
```

### Mod 2 — Agent (Hibrit Akıllı Analiz)
```
┌─────────────┐     ┌──────────────────────────────────────────────────────┐
│  Kullanıcı  │     │  Hibrit Pipeline                                     │
│  CV + İlan  │────▶│                                                      │
│             │     │  1. beceri_cikar(cv)   ─┐                            │
│             │     │  2. beceri_cikar(ilan)  ├─▶ Programatik tool çağrısı │
│             │     │  3. karsilastir         │                            │
│             │     │  4. skor_hesapla       ─┘                            │
│             │     │  5. LLM → Kişisel değerlendirme (llama3.1)           │
│             │◀────│                                                      │
│  Takip      │────▶│  6. Takip soruları → LLM (konuşma geçmişi ile)       │
└─────────────┘     └──────────────────────────────────────────────────────┘
```

1. **Girdi**: Kullanıcı CV metnini ve iş ilanı metnini girer
2. **Mod seçimi**: Chain (sabit akış) veya Agent (hibrit akıllı analiz)
3. **Analiz**: Chain → tek seferde LLM / Agent → programatik tool'lar + LLM değerlendirme
4. **Çıktı**: Eşleşen/eksik beceriler, uyum skoru ve kişisel değerlendirme
5. **Takip** (Agent): Konuşma geçmişi korunarak ek soru sorulabilir

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
| **2 — Agent Yapısı** | ✅ Tamamlandı | Tool kullanan agent, takip soruları, akıllı kariyer önerileri |
| **3 — Ürünleştirme** | 📋 Planlandı | Streamlit arayüz, PDF yükleme, demo yapılabilir hale getirme |

### Aşama 1 — Temel MVP ✅
- [x] LangChain + Ollama entegrasyonu
- [x] PromptTemplate ile yapılandırılmış analiz
- [x] LCEL chain (pipe operatörü)
- [x] Dosyadan veya elle metin girişi
- [x] Beceri eşleştirme ve eksik analizi
- [x] Uyum skoru hesaplama

### Aşama 2 — Agent ve Akıllı Analiz ✅
- [x] Hibrit agent: programatik tool çağrıları + LLM değerlendirme
- [x] 4 tool: beceri_cikar (bilinen beceri DB'si), karsilastir (fuzzy matching), skor_hesapla, oneri_uret
- [x] 40+ teknik beceri tanıma (KNOWN_SKILLS veritabanı)
- [x] Takip soruları — konuşma geçmişi korunarak (LLM chat modu)
- [x] Kısmi beceri eşleştirme (substring + kelime bazlı fuzzy matching)
- [x] Tool sonuçları ekranda adım adım gösterim

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
| **LangGraph** | Agent yapısı (create_agent, ReAct döngüsü) |
| **Ollama** | Yerel LLM çalıştırma altyapısı |
| **Llama 3 / 3.1** | Dil modelleri (3: chain, 3.1: agent tool calling) |
| **uv** | Paket ve proje yönetimi |

---

## 👩‍💻 Geliştirici

**Rumeysa Sakın**
- Endüstri Mühendisi | Endüstri Mühendisliği Yüksek Lisans Öğrencisi
- Kariyer Odağı: İş Analisti · Product Manager · AI Engineer

---

## 📝 Lisans

Bu proje eğitim ve portföy amaçlı geliştirilmiştir.
