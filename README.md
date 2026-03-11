# 🔍 AI Kariyer Asistanı

> CV'nizi bir iş ilanıyla karşılaştırın — eşleşen becerileri, eksikleri ve somut kariyer önerilerini görün.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL%20%2B%20Tools-green.svg)](https://langchain.com)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-orange.svg)](https://ollama.com)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](#docker-ile-çalıştırma)

---

## Proje Özeti

AI Kariyer Asistanı, CV metni ile iş ilanı metnini karşılaştırarak beceri uyumunu analiz eden bir yapay zeka prototipidir. Tamamen yerel çalışır — API anahtarı veya ücretli servis gerektirmez.

**Ne yapar:**
- CV ve iş ilanından teknik becerileri çıkarır (40+ beceri, alias normalization)
- Beceri eşleştirmesi yapar (fuzzy matching ile)
- Uyum skoru hesaplar
- Her eksik beceri için somut, portföy odaklı öneriler üretir
- Kişisel kariyer değerlendirmesi yazar (LLM ile)

**İki analiz modu:**
- **Chain** — Tek LLM çağrısı ile hızlı analiz
- **Agent** — Deterministik tool pipeline + LLM değerlendirme (hibrit yaklaşım)

---

## Özellikler

| Özellik | Açıklama |
|---------|----------|
| **Beceri Çıkarma** | 40+ teknik beceri tanıma, alias normalization (ör: `restful api` → `rest api`, `k8s` → `kubernetes`) |
| **Fuzzy Matching** | Substring + kelime kesişimi ile kısmi eşleştirme |
| **Öneri Motoru** | 40+ beceriye özel somut öneriler — mini proje, araç ve portföy tavsiyeleri |
| **Uyum Skoru** | Programatik hesaplama (eşleşen / toplam × 100) |
| **Takip Soruları** | Agent modunda konuşma geçmişi korunarak LLM ile sohbet (terminal) |
| **Web Arayüzü** | Streamlit ile kullanıcı dostu arayüz |
| **Docker Desteği** | Tek komutla çalıştırılabilir konteyner |

---

## Mimari

### Chain Modu (Hızlı)

```
Kullanıcı → PromptTemplate → Ollama (Llama 3) → Markdown rapor
```

Tek LLM çağrısı. Hızlı ama her çalıştırmada sonuç farklı olabilir.

### Agent Modu (Hibrit)

```
Kullanıcı → [beceri_cikar → karsilastir → skor_hesapla → oneri_uret] → LLM değerlendirme → Rapor
                              ↑ Programatik tool çağrıları ↑              ↑ Yalnız yorum ↑
```

Tool'lar deterministik çalışır (aynı girdi → aynı çıktı). LLM yalnızca kişisel değerlendirme yazmak için kullanılır. Bu yaklaşım küçük modellerin tool calling tutarsızlığını ortadan kaldırır.

### Chain vs Agent Karşılaştırma

| Özellik | Chain | Agent |
|---------|-------|-------|
| Model | Llama 3 | Llama 3.1 |
| Beceri Tanıma | LLM'e bırakılır | KNOWN_SKILLS DB + alias normalization |
| Eşleştirme | LLM yorumu | Fuzzy matching (deterministik) |
| Skor | LLM tahmini | Programatik hesaplama |
| Öneriler | Genel LLM önerileri | Beceriye özel somut öneriler (40+) |
| Takip Soruları | Yok | Konuşma geçmişi ile sohbet |
| Tekrarlanabilirlik | Düşük | Yüksek |

---

## Hızlı Başlangıç

### Gereksinimler

| Araç | Açıklama |
|------|----------|
| [Python 3.11+](https://python.org) | Programlama dili |
| [uv](https://docs.astral.sh/uv/) | Paket yöneticisi |
| [Ollama](https://ollama.com) | Yerel LLM çalıştırıcı |

### Kurulum

```bash
# 1. Repoyu klonlayın
git clone https://github.com/rumeysasakin/ai-career-copilot.git
cd ai-career-copilot

# 2. Bağımlılıkları yükleyin
uv sync

# 3. Ollama modellerini indirin
ollama pull llama3       # Chain modu için
ollama pull llama3.1     # Agent modu için

# 4. Sanal ortamı aktive edin
# Windows:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate
```

### Terminal ile Çalıştırma

```bash
python main.py
```

İki mod sunulur: Chain (hızlı) veya Agent (detaylı). Örnek CV ve iş ilanı dosyaları hazır gelir.

### Streamlit ile Çalıştırma

```bash
streamlit run streamlit_app.py
```

Tarayıcıda `http://localhost:8501` adresinde açılır:

```
┌─────────────────────────────────────────────────────────┐
│  🔍 AI Kariyer Asistanı                                │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  📄 CV Metni    │  │  📋 İlan Metni  │              │
│  │  [text area]    │  │  [text area]    │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  ○ Agent Modu  ○ Chain Modu    [🔍 Analiz Et]          │
│                                                         │
│  ┌──────────────────────────────────────────┐          │
│  │  📊 Eşleşen: 11/20  Skor: %55  Eksik: 9 │          │
│  │  [Eşleşen] [Eksik] [Öneriler] [Değerl.]  │          │
│  └──────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

---

## Docker ile Çalıştırma

> **Not:** Ollama host makinede çalışmalıdır. Container yalnızca Streamlit uygulamasını çalıştırır ve Ollama'ya `host.docker.internal` üzerinden bağlanır.

```bash
# 1. Ollama'nın host makinede çalıştığından emin olun
ollama serve

# 2. Container'ı başlatın
docker compose up --build

# 3. Tarayıcıda açın
# http://localhost:8501
```

Ollama farklı bir adreste çalışıyorsa:

```bash
OLLAMA_HOST=http://192.168.1.100:11434 docker compose up --build
```

---

## Örnek Çıktı (Agent Modu)

`ornek_cv.txt` ve `ornek_ilan.txt` ile üretilen gerçek çıktı:

```
🤖 Agent modu aktif — Tool çağrıları:

  🔧 beceri_cikar(cv) çağrılıyor...
    → [CV] Bulunan beceriler (17): css, django, docker, flask, git, html,
      javascript, linux, postgresql, python, react, rest api, sql, sqlite ...

  🔧 beceri_cikar(ilan) çağrılıyor...
    → [ILAN] Bulunan beceriler (17): celery, ci/cd, django, docker, fastapi,
      git, github actions, jenkins, kubernetes, microservices, mysql,
      postgresql, pytest, python, rabbitmq, redis, rest api ...

  🔧 karsilastir çağrılıyor...
    → Eşleşen (9): django, docker, git, postgresql, python, rest api, sql ...
      Eksik (8): celery, ci/cd, fastapi, jenkins, kubernetes, pytest, redis ...

  🔧 skor_hesapla çağrılıyor...
    → Uyum Skoru: %53 — Orta uyum

  🔧 oneri_uret çağrılıyor...
    → Somut Öneriler:
      - fastapi: FastAPI ile küçük REST API projesi oluşturun. GitHub'a yükleyin.
      - ci/cd: GitHub Actions ile test + lint pipeline'ı ekleyin.
      - kubernetes: Minikube ile K8s cluster kurun. Pod deploy edin.
      - pytest: En önemli 3 fonksiyon için unit test yazın. CI'a entegre edin.
      - redis: Django projenize redis cache ekleyin.
      ...

  🤖 Kişisel değerlendirme yazılıyor...

📊 Uyum Skoru: %53 — Orta uyum. Eksik becerilere odaklanmanız gerekiyor.
```

---

## Proje Yapısı

```
ai-career-copilot/
├── core/                      # Analiz motoru
│   ├── __init__.py
│   ├── skills.py              # Beceri DB, normalization, extraction
│   ├── tools.py               # LangChain tool'ları (@tool)
│   ├── chain.py               # Chain modu (PromptTemplate + LCEL)
│   └── agent.py               # Agent modu (hibrit pipeline)
├── streamlit_app.py           # Web arayüzü
├── main.py                    # Terminal CLI
├── ornek_cv.txt               # Örnek CV
├── ornek_ilan.txt             # Örnek iş ilanı
├── Dockerfile                 # Container tanımı
├── docker-compose.yml         # Orkestrasyon
├── .streamlit/config.toml     # Streamlit ayarları
├── pyproject.toml             # Proje yapılandırması
├── docs/                      # Dokümantasyon
│   ├── product_perspective.md
│   ├── business_analysis.md
│   └── technical_architecture.md
└── README.md
```

---

## Proje Durumu

| Alan | Durum | Detay |
|------|-------|-------|
| Beceri Çıkarma | ✅ Çalışıyor | 40+ beceri, alias normalization |
| Fuzzy Matching | ✅ Çalışıyor | Substring + kelime kesişimi |
| Öneri Motoru | ✅ Rule-based | 40+ beceriye özel somut öneriler |
| Chain Modu | ✅ Çalışıyor | Llama 3, tek LLM çağrısı |
| Agent Modu | ✅ Çalışıyor | Hibrit pipeline, deterministik tool'lar |
| Takip Soruları | ✅ Terminal | Konuşma geçmişi korunarak sohbet |
| Web Arayüzü | ✅ Streamlit | Agent + Chain modu, metrikler, sekmeler |
| Docker | ✅ Hazır | Tek komutla çalıştırılabilir |
| PDF Desteği | 📋 Planlanıyor | PDF'den CV okuma |

> **Not:** Beceri tanıma rule-based (keyword matching + alias normalization) çalışmaktadır. NLP/ML tabanlı extraction ileride planlanmaktadır.

---

## Yol Haritası

- [x] PromptTemplate + LCEL chain ile temel analiz
- [x] Hibrit agent: programatik tool'lar + LLM değerlendirme
- [x] 40+ beceri tanıma + alias normalization
- [x] Beceriye özel somut öneriler (ONERI_HARITASI)
- [x] Fuzzy matching (substring + kelime kesişimi)
- [x] Takip soruları (konuşma geçmişi korunarak)
- [x] Streamlit web arayüzü
- [x] Docker desteği
- [ ] PDF'den CV yükleme
- [ ] Çoklu ilan karşılaştırma
- [ ] NLP tabanlı beceri çıkarma

---

## Teknoloji Stack

| Teknoloji | Kullanım |
|-----------|----------|
| Python 3.11 | Ana dil |
| LangChain | LLM orchestration (LCEL chain + @tool) |
| Ollama | Yerel LLM (Llama 3 / 3.1) |
| Streamlit | Web arayüzü |
| Docker | Konteynerizasyon |
| uv | Paket yönetimi |

---

## Dokümantasyon

| Doküman | Perspektif |
|---------|-----------|
| [Product Perspective](docs/product_perspective.md) | Product Manager — problem, kullanıcı segmentleri, metrikler |
| [Business Analysis](docs/business_analysis.md) | İş Analisti — gereksinimler, use case, kabul kriterleri |
| [Technical Architecture](docs/technical_architecture.md) | AI Engineer — mimari, model seçimi, teknik kararlar |

---

## Geliştirici

**Rumeysa Sakın**
Endüstri Mühendisi · Endüstri Mühendisliği Yüksek Lisans Öğrencisi
Kariyer Odağı: İş Analisti · Product Manager · AI Engineer

---

## Lisans

Bu proje eğitim ve portföy amaçlı geliştirilmiştir.
