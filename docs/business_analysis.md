# 📊 Business Analysis — İş Analisti Bakış Açısı

> Bu doküman, AI Kariyer Asistanı projesini bir İş Analisti'nin (Business Analyst / Technical BA) gözünden inceler.

---

## 1. Proje Tanımı

| Alan | Değer |
|------|-------|
| **Proje Adı** | AI Kariyer Asistanı — CV & İş İlanı Eşleştirme Sistemi |
| **Amaç** | Kullanıcının CV'si ile iş ilanı arasındaki beceri uyumunu analiz etmek |
| **Paydaşlar** | İş arayanlar, kariyer danışmanları, İK profesyonelleri |
| **Mevcut Aşama** | Aşama 2 — Agent (Hibrit Akıllı Analiz) |

---

## 2. İş Gereksinimleri (Business Requirements)

### BR-01: Beceri Eşleştirme
**Açıklama:** Sistem, CV'deki becerileri ve iş ilanındaki gereksinimleri çıkarıp karşılaştırabilmelidir.
**Kabul Kriteri:** Sistem en az 5 farklı CV-ilan çiftiyle test edildiğinde %80 doğrulukla becerileri eşleştirebilmelidir.
**Öncelik:** Yüksek (Must Have)

### BR-02: Eksik Beceri Tespiti
**Açıklama:** Sistem, ilanda aranan ancak CV'de bulunmayan becerileri listeleyebilmelidir.
**Kabul Kriteri:** Eksik beceriler ayrı bir bölümde, madde madde gösterilmelidir.
**Öncelik:** Yüksek (Must Have)

### BR-03: Kariyer Önerileri
**Açıklama:** Sistem, eksik becerilerin nasıl kapatılabileceğine dair somut öneriler sunabilmelidir.
**Kabul Kriteri:** Her eksik beceri için en az bir aksiyon önerisi verilmelidir.
**Öncelik:** Orta (Should Have)

### BR-04: Uyum Skoru
**Açıklama:** Sistem, CV-ilan uyumunu yüzdesel bir skorla ifade edebilmelidir.
**Kabul Kriteri:** 0-100 arası bir skor ve kısa bir açıklama verilmelidir.
**Öncelik:** Orta (Should Have)

### BR-05: Çoklu Girdi Desteği
**Açıklama:** Kullanıcı metin girişini dosyadan veya elle yapabilmelidir.
**Kabul Kriteri:** Her iki yöntemle de sorunsuz çalışmalıdır.
**Öncelik:** Düşük (Nice to Have)

---

## 3. Fonksiyonel Gereksinimler (Functional Requirements)

### FR-01: CV Metni Alma
| Alan | Değer |
|------|-------|
| **Girdi** | Düz metin formatında CV |
| **Kaynak** | Dosyadan (.txt) veya kullanıcı girişi |
| **Doğrulama** | Boş metin kabul edilmez |

### FR-02: İş İlanı Metni Alma
| Alan | Değer |
|------|-------|
| **Girdi** | Düz metin formatında iş ilanı |
| **Kaynak** | Dosyadan (.txt) veya kullanıcı girişi |
| **Doğrulama** | Boş metin kabul edilmez |

### FR-03: LLM Tabanlı Analiz
| Alan | Değer |
|------|-------|
| **Girdi** | CV metni + İlan metni |
| **İşlem** | Hibrit pipeline: programatik tool çağrıları + LLM değerlendirme |
| **Çıktı** | Yapılandırılmış analiz sonucu + kişisel değerlendirme |
| **Model** | Llama 3 (chain) / Llama 3.1 (agent) via Ollama |
| **Parametre** | temperature=0.3 |

### FR-04: Sonuç Gösterimi
| Alan | Değer |
|------|-------|
| **Format** | Markdown benzeri yapılandırılmış metin |
| **Bölümler** | CV becerileri, ilan gereksinimleri, eşleşenler, eksikler, öneriler, skor |
| **Kanal** | Terminal çıktısı |

---

## 4. Fonksiyonel Olmayan Gereksinimler (Non-Functional Requirements)

| ID | Gereksinim | Hedef |
|----|-----------|-------|
| **NFR-01** | Yanıt süresi | < 60 saniye (yerel model ile) |
| **NFR-02** | Gizlilik | Tüm veriler yerel kalır, dış servise gönderilmez |
| **NFR-03** | Taşınabilirlik | Windows, Linux, macOS üzerinde çalışır |
| **NFR-04** | Dil desteği | Türkçe CV ve ilanları destekler |
| **NFR-05** | Bağımlılık | İnternet bağlantısı gerektirmez (model indirildikten sonra) |

---

## 5. Use Case Diyagramı

### UC-01: CV-İlan Karşılaştırma (Ana Senaryo)

| Alan | Değer |
|------|-------|
| **Aktör** | İş arayan kullanıcı |
| **Ön Koşul** | Ollama çalışıyor, Llama3 modeli indirilmiş |
| **Tetikleyici** | Kullanıcı programı çalıştırır |

**Ana Akış:**
```
1. Kullanıcı programı başlatır
2. Sistem CV girdi yöntemini sorar (dosya/elle)
3. Kullanıcı CV metnini sağlar
4. Sistem iş ilanı girdi yöntemini sorar (dosya/elle)
5. Kullanıcı iş ilanı metnini sağlar
6. Sistem metinleri LLM'e gönderir
7. LLM analiz sonucunu üretir
8. Sistem sonucu ekrana yazdırır
```

**Alternatif Akış:**
```
3a. Dosya bulunamazsa → Hata mesajı gösterilir
6a. Ollama çalışmıyorsa → Bağlantı hatası gösterilir
7a. Model yanıt üretemezse → Timeout hatası gösterilir
```

**Son Koşul:** Kullanıcı analiz sonucunu ekranda görür.

---

## 6. Veri Akış Diyagramı (Data Flow)

```
┌──────────────────────────────────────────────────────────┐
│                         SİSTEM                           │
│                                                          │
│  ┌─────────┐    ┌───────────────┐    ┌────────────────┐  │
│  │ CV.txt  │───▶│               │    │                │  │
│  └─────────┘    │  PromptTemp.  │───▶│  Ollama/Llama3 │  │
│  ┌─────────┐    │  (Şablon      │    │  (Analiz)      │  │
│  │İlan.txt │───▶│   Doldurma)   │    │                │  │
│  └─────────┘    └───────────────┘    └───────┬────────┘  │
│                                              │           │
│                                              ▼           │
│                                     ┌────────────────┐   │
│                                     │  Yapılandırılmış│  │
│                                     │  Analiz Çıktısı │  │
│                                     └────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 7. İş Kuralları (Business Rules)

| ID | Kural | Açıklama |
|----|-------|----------|
| **BK-01** | Beceri eşleştirme semantik olmalı | "Python" ve "Python programlama" aynı beceri olarak değerlendirilmeli |
| **BK-02** | Skor 0-100 arası olmalı | Yüzdesel ifade, kısa açıklamayla |
| **BK-03** | Öneriler somut olmalı | "Daha çok çalış" değil, "pytest ile 3 birim test yazarak başla" gibi |
| **BK-04** | Veri yerel kalmalı | Hiçbir CV/ilan verisi dış servise gönderilmemeli |
| **BK-05** | Türkçe yanıt | Analiz sonuçları Türkçe olmalı |

---

## 8. MOSCOW Önceliklendirme

### Must Have (Olmazsa Olmaz)
- CV metni girişi
- İlan metni girişi
- Beceri eşleştirme analizi
- Eksik beceri listesi

### Should Have (Olması Gereken)
- Uyum skoru
- Somut öneriler
- Dosyadan okuma desteği

### Could Have (Olsa İyi Olur)
- Yapılandırılmış JSON çıktı
- Birden fazla ilan karşılaştırma
- Analiz geçmişi

### Won't Have (Bu Aşamada Olmayacak)
- Web arayüzü (Aşama 3'te)
- PDF yükleme (Aşama 3'te)
- Kullanıcı hesapları
- Veritabanı depolama

---

## 9. Aşamalar Arası Gereksinim Evrimi

| Gereksinim | Aşama 1 (MVP) | Aşama 2 (Agent) | Aşama 3 (Ürün) |
|-----------|----------------|-----------------|-----------------|
| Girdi yöntemi | Metin (dosya/elle) | Metin + interaktif | Metin + PDF + Web form |
| Analiz tipi | Tek seferlik | Diyalog tabanlı | Diyalog + çoklu ilan |
| Çıktı formatı | Düz metin | Yapısal (JSON) | Web UI + dışa aktarım |
| Etkileşim | Tek yönlü | Çift yönlü (takip sorusu) | Tam interaktif |
| Dağıtım | Terminal (yerel) | Terminal (yerel) | Web (Streamlit) |

---

## 10. Kabul Test Senaryoları

### Aşama 1 Testleri

| Test ID | Senaryo | Beklenen Sonuç | Durum |
|---------|---------|----------------|-------|
| **AT-01** | Örnek CV + örnek ilan dosyalarıyla çalıştır | 6 bölümlü analiz çıktısı | ✅ Geçti |
| **AT-02** | Elle CV + elle ilan girişi | 6 bölümlü analiz çıktısı | ✅ Geçti |
| **AT-03** | Türkçe CV + Türkçe ilan | Türkçe analiz sonucu | ✅ Geçti |
| **AT-04** | Farklı sektörden CV-ilan çifti | Düşük uyum skoru, çok sayıda eksik | ✅ Geçti |
| **AT-05** | Çok benzer CV-ilan çifti | Yüksek uyum skoru, az eksik | ✅ Geçti |

### Aşama 2 Testleri

| Test ID | Senaryo | Beklenen Sonuç | Durum |
|---------|---------|----------------|-------|
| **AT-06** | Agent moduyla (mod 2) örnek dosyalarla analiz | Tool çağrıları + yapısal rapor + kişisel değerlendirme | ✅ Geçti |
| **AT-07** | Takip sorusu sorma (agent mod) | Bağlama uygun, tutarlı cevap | ✅ Geçti |
| **AT-08** | Beceri eşleştirme doğruluğu (fuzzy) | REST API ↔ RESTful API eşleşmeli | ✅ Geçti |
| **AT-09** | Tool sonuçları ekranda görünürlük | Her tool çağrısı adım adım yazdırılmalı | ✅ Geçti |
| **AT-10** | Mod 1 (chain) geriye uyumluluk | Eski chain modu hala çalışmalı | ✅ Geçti |
