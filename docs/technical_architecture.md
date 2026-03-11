# 🧠 Technical Architecture — AI Engineer Bakış Açısı

> Bu doküman, AI Kariyer Asistanı projesini bir AI Engineer'ın gözünden inceler. Mimari kararlar, model seçimi, prompt engineering ve teknik detaylar bu dokümanda yer alır.

---

## 1. Sistem Mimarisi

### Genel Bakış

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Kariyer Asistanı                      │
│                                                                 │
│   ┌──────────┐    ┌──────────────┐    ┌──────────┐    ┌──────┐ │
│   │  Input    │    │  LangChain   │    │  Ollama  │    │Output│ │
│   │  Layer    │───▶│  LCEL Chain  │───▶│  Server  │───▶│Layer │ │
│   │          │    │              │    │  (Local) │    │      │ │
│   │ -CV txt  │    │ -PromptTemp. │    │ -Llama3  │    │-Term.│ │
│   │ -İlan txt│    │ -Pipe (|)    │    │ -8B param│    │-Print│ │
│   └──────────┘    └──────────────┘    └──────────┘    └──────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Bileşen Detayları

| Bileşen | Teknoloji | Rol |
|---------|-----------|-----|
| **Input Layer** | Python I/O | Kullanıcıdan metin alma (dosya/stdin) |
| **Orchestration** | LangChain LCEL | Prompt oluşturma + LLM çağrısı zinciri |
| **LLM Runtime** | Ollama | Yerel model sunucusu (HTTP API: localhost:11434) |
| **Model** | Llama 3 / 3.1 8B | Meta'nın açık kaynak dil modelleri (3: chain, 3.1: agent) |
| **Output** | Terminal (stdout) | Yapılandırılmış metin çıktısı |

---

## 2. Teknoloji Seçimi ve Gerekçeler

### Neden LangChain?
| Alternatif | Avantaj | Dezavantaj | Karar |
|-----------|---------|------------|-------|
| **LangChain** | Geniş ekosistem, LCEL, agent desteği | Öğrenme eğrisi | ✅ Seçildi |
| Doğrudan API çağrısı | Basitlik | Ölçeklenmiyor, agent yok | ❌ |
| LlamaIndex | RAG için güçlü | Analiz odaklı değil | ❌ |
| Haystack | Pipeline yapısı | Daha az topluluk desteği | ❌ |

**Gerekçe:** Proje ilerleyen aşamalarda agent, tool calling ve RAG kullanacak. LangChain bu özelliklerin tamamını destekler ve geçiş maliyetini minimize eder.

### Neden Ollama + Llama 3?
| Alternatif | Avantaj | Dezavantaj | Karar |
|-----------|---------|------------|-------|
| **Ollama + Llama 3** | Ücretsiz, yerel, gizli | Donanım gerekir | ✅ Seçildi |
| OpenAI API | Güçlü modeller | Ücretli, veri dışarı çıkar | ❌ |
| Hugging Face (local) | Esneklik | Kurulum karmaşık | ❌ |
| Google Gemini | Ücretsiz tier | API bağımlılığı | ❌ |

**Gerekçe:** Proje eğitim ve portföy amaçlı. Veri gizliliği ve maliyet önemli. Ollama kolay kurulum + yerel çalışma sunuyor.

### Neden LCEL (LangChain Expression Language)?
```python
# Eski yöntem (LLMChain - deprecated)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(input)

# Yeni yöntem (LCEL - pipe operatörü)
chain = prompt | llm
result = chain.invoke(input)
```

LCEL tercih edildi çünkü:
- LangChain'in **güncel ve önerilen** yaklaşımı
- Daha **okunabilir** ve **composable** (birleştirilebilir)
- Streaming, batch, async desteği hazır
- Aşama 2'de `prompt | llm | output_parser` gibi kolayca genişletilebilir

---

## 3. Prompt Engineering

### Prompt Tasarım İlkeleri

Bu projede uygulanan prompt engineering teknikleri:

#### 1. Rol Atama (Role Prompting)
```
"Sen bir kariyer danışmanısın."
```
LLM'e belirli bir uzmanlık alanı atamak, daha tutarlı ve konuya odaklı cevaplar üretir.

#### 2. Görev Ayrıştırma (Task Decomposition)
```
"Görevlerin:
1. CV'deki becerileri çıkar
2. İlandaki gereksinimleri çıkar
3. Eşleşenleri bul
4. Eksikleri bul
5. Öneriler ver"
```
Tek büyük görev yerine 5 alt göreve bölmek, LLM'in sistematik çalışmasını sağlar.

#### 3. Çıktı Formatı Belirtme (Output Formatting)
```
"## ✅ Eşleşen Beceriler
- (madde madde listele)"
```
Prompt'ta istenen çıktı formatını açıkça belirtmek, yapılandırılmış sonuç garanti eder.

#### 4. Bağlam Ayırma (Context Separation)
```
"---
CV METNİ:
{cv_metni}
---
İŞ İLANI METNİ:
{ilan_metni}"
```
İki farklı metni ayırıcılarla (---) birbirinden net şekilde ayırmak, LLM'in karıştırmasını önler.

### Prompt Parametreleri

| Parametre | Değer | Gerekçe |
|-----------|-------|---------|
| **temperature** | 0.3 | Analiz görevi → düşük yaratıcılık, yüksek tutarlılık |
| **model** | llama3 / llama3.1 | 8B parametre, llama3: chain, llama3.1: agent (tool calling) |

> **Not:** `temperature=0` tam deterministik yapar ama bazen tekrarlı çıktılar üretir. 0.3 dengeli bir değerdir.

---

## 4. LangChain LCEL Chain Yapısı

### Mevcut Chain (Aşama 1)

```python
analiz_chain = analiz_prompt | llm
```

```
PromptTemplate ──pipe──▶ ChatOllama
     │                        │
     │ input_variables:       │ model: llama3
     │   - cv_metni           │ temperature: 0.3
     │   - ilan_metni         │
     │                        │
     ▼                        ▼
  Doldurulmuş          AIMessage objesi
  prompt string        (content: analiz metni)
```

### Planlanan Chain (Aşama 2) → ✅ Tamamlandı

```python
# Hibrit yaklaşım benimsenmiştir:
# Tool'lar programatik olarak çağrılır, LLM sadece rapor/değerlendirme yazar.
analiz_chain = analiz_prompt | llm  # Chain modu (Llama 3)
# Agent modu: tool sonuçları + llm.invoke(yorum_prompt)  (Llama 3.1)
```

### Agent Yapısı (Aşama 2) → ✅ Tamamlandı

```python
# Hibrit agent: tool'lar programatik çağrılır, LLM sadece değerlendirme yazar
from tools import beceri_cikar, karsilastir, skor_hesapla, oneri_uret

# 1. Tool'lar sırayla çağrılır (güvenilir, deterministik)
cv_beceriler = beceri_cikar.invoke({"metin": cv, "kaynak": "cv"})
ilan_beceriler = beceri_cikar.invoke({"metin": ilan, "kaynak": "ilan"})
karsilastirma = karsilastir.invoke({"cv_skills": ..., "job_skills": ...})
skor = skor_hesapla.invoke({"eslesen": n, "toplam": m})

# 2. LLM sadece kişisel değerlendirme yazar
yorum = llm.invoke(yorum_prompt)  # Llama 3.1

# 3. Takip soruları için LLM chat modu (konuşma geçmişiyle)
yanit = llm.invoke(gecmis_mesajlar)
```

> **Neden hibrit?** `llama3.1 8B` tool calling API'sini tutarsız kullanıyor (bazen tool çağırmak yerine JSON yazıyor). Tool'ları programatik çağırmak %100 güvenilirlik sağlıyor.

---

## 5. Veri Akışı (Data Pipeline)

### Aşama 1 — Akış Detayı

```
Adım 1: Girdi Toplama
────────────────────
  Kullanıcı → dosyadan_oku("ornek_cv.txt") → cv_metni: str
  Kullanıcı → dosyadan_oku("ornek_ilan.txt") → ilan_metni: str

Adım 2: Prompt Doldurma
────────────────────────
  PromptTemplate.format(cv_metni=..., ilan_metni=...) → prompt_str: str
  
  Girdi: {"cv_metni": "...", "ilan_metni": "..."}
  Çıktı: "Sen bir kariyer danışmanısın. Sana bir CV... [doldurlmuş metin]"

Adım 3: LLM Çağrısı
─────────────────────
  ChatOllama.invoke(prompt_str) → AIMessage
  
  HTTP POST → http://localhost:11434/api/chat
  Model: llama3
  Temperature: 0.3

Adım 4: Çıktı
──────────────
  AIMessage.content → str → print()
```

---

## 6. Performans ve Sınırlamalar

### Mevcut Performans (Aşama 1)

| Metrik | Değer | Notlar |
|--------|-------|--------|
| İlk yanıt süresi | ~15-45 sn | Donanıma bağlı (GPU varsa daha hızlı) |
| Token limiti | ~8192 token | Llama3 8B context window |
| Bellek kullanımı | ~5-8 GB RAM | Model yüklü iken |
| GPU gereksinimi | Opsiyonel | CPU'da da çalışır (daha yavaş) |

### Bilinen Sınırlamalar

| Sınırlama | Açıklama | Çözüm Planı |
|-----------|----------|-------------|
| Çıktı tutarsızlığı | Aynı girdiyle farklı formatlar | ✅ Hibrit yaklaşım ile çözüldü (tool'lar deterministik) |
| Tek seferlik analiz | Takip sorusu sorulanamıyor | ✅ Aşama 2'de konuşma geçmişi ile çözüldü |
| Sadece metin girişi | PDF desteklenmiyor | Aşama 3: PDF parser |
| Hallüsinasyon riski | LLM uydurma beceri yazabilir | ✅ KNOWN_SKILLS DB ile çözüldü (40+ bilinen beceri) |
| Dil karışması | Türkçe soru → İngilizce cevap | Prompt'ta "Türkçe yanıt ver" zorlaması |
| Tool calling tutarsızlığı | llama3.1 8B bazen tool çağırmak yerine JSON yazıyor | ✅ Hibrit yaklaşımla çözüldü (programatik tool çağrısı) |

---

## 7. Güvenlik ve Gizlilik

| Konu | Durum | Açıklama |
|------|-------|----------|
| Veri gizliliği | ✅ Güvenli | Tüm veriler yerel kalır |
| Dış API çağrısı | ❌ Yok | Ollama localhost'ta çalışır |
| CV verisi depolama | ❌ Saklanmıyor | İşlem sonrası bellekten silinir |
| Model güvenliği | ✅ Güvenli | Llama 3 açık kaynak, doğrulanmış |

---

## 8. Aşama 2 Teknik Tasarım (Planlanan)

### Agent Mimarisi

```
┌─────────────────────────────────────────────────────┐
│                    AgentExecutor                     │
│                                                     │
│   ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│   │  Agent   │───▶│ Reasoning│───▶│ Tool Seçimi  │  │
│   │  (LLM)   │◀───│ Loop     │◀───│ & Çalıştırma │  │
│   └──────────┘    └──────────┘    └──────────────┘  │
│                                          │          │
│                        ┌─────────────────┤          │
│                        ▼                 ▼          │
│                ┌──────────────┐  ┌──────────────┐   │
│                │beceri_cikar  │  │oneri_uret    │   │
│                │Tool          │  │Tool          │   │
│                └──────────────┘  └──────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Plananan Tool'lar

```python
@tool
def beceri_cikar(metin: str) -> list[str]:
    """Bir metinden teknik ve soft skill becerileri çıkarır."""

@tool  
def uyum_skoru_hesapla(eslesenler: list, eksikler: list) -> dict:
    """Eşleşen ve eksik becerilere göre uyum skoru hesaplar."""

@tool
def kariyer_onerisi(eksik_beceriler: list, mevcut_deneyim: str) -> str:
    """Eksik becerilere göre kişiselleştirilmiş kariyer önerisi üretir."""
```

---

## 9. Geliştirme Ortamı

| Araç | Versiyon | Kullanım |
|------|----------|----------|
| Python | 3.11+ | Ana dil |
| uv | Son sürüm | Paket yönetimi |
| Ollama | Son sürüm | LLM sunucusu |
| LangChain | >=1.2.10 | Orchestration |
| langchain-ollama | >=1.0.1 | Ollama entegrasyonu |
| VS Code | Son sürüm | IDE |
| Git | Son sürüm | Versiyon kontrol |

### Bağımlılıklar (pyproject.toml)

```toml
dependencies = [
    "langchain>=1.2.10",
    "langchain-community>=0.4.1",
    "langchain-ollama>=1.0.1",
    "langchain-openai>=1.1.11",
]
```

---

## 10. Öğrenilen Dersler (Aşama 1)

| Konu | Öğrenilen |
|------|-----------|
| **LCEL vs LLMChain** | LCEL daha modern ve esnek. LLMChain deprecated. |
| **Prompt formatı** | Çıktı formatını prompt'ta açıkça belirtmek sonucu iyileştirir |
| **Temperature** | Analiz görevleri için düşük (0.2-0.4), yaratıcı görevler için yüksek (0.7-0.9) |
| **Yerel model** | Ollama kurulumu basit; 8GB RAM yeterli; GPU varsa çok hızlanıyor |
| **invoke() kullanımı** | Sözlük (dict) formatında parametre gönderilmeli: `chain.invoke({"key": "value"})` |
