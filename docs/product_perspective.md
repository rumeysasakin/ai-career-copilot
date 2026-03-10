# 📦 Product Perspective — Ürün Yöneticisi Bakış Açısı

> Bu doküman, AI Kariyer Asistanı projesini bir Product Manager'ın gözünden inceler.

---

## 1. Problem Tanımı

### Mevcut Durum (As-Is)
İş arayanlar şu sorunlarla karşılaşıyor:
- Bir ilana ne kadar uyduklarını **objektif olarak değerlendiremiyorlar**
- CV'deki becerileri ile ilandaki gereksinimleri **manuel olarak karşılaştirmak** zaman alıyor
- Hangi becerileri geliştirmeleri gerektiğini **sistematik olarak göremiyorlar**
- Başvuru öncesi hazırlık süreci **subjektif ve verimsiz**

### Hedef Durum (To-Be)
- Kullanıcı CV'sini ve hedeflediği ilanı girer
- Sistem **saniyeler içinde** objektif bir analiz sunar
- Eşleşen beceriler, eksikler ve somut öneriler **yapılandırılmış bir formatta** gösterilir
- Kullanıcı **neye odaklanması gerektiğini** net olarak bilir

### Problem Statement
> "İş arayanlar, bir ilana başvurmadan önce mevcut becerilerinin ilana ne kadar uyduğunu hızlı ve objektif bir şekilde değerlendiremiyorlar. Bu durum; uygun olmayan ilanlara başvuru yapılmasına, güçlü adayların kendilerini eksik hissetmesine veya gerçek eksiklerin fark edilmemesine yol açıyor."

---

## 2. Hedef Kullanıcı Segmentleri

| Segment | Açıklama | Temel İhtiyaç |
|---------|----------|---------------|
| **Yeni Mezunlar** | İlk işini arayan, deneyimi sınırlı kişiler | "Hangi becerileri edinmeliyim?" |
| **Kariyer Değiştirenler** | Farklı bir alana geçiş yapanlar | "Mevcut becerilerim yeni alanda işe yarar mı?" |
| **Deneyimli Profesyoneller** | Üst pozisyonlara başvuranlar | "Bu pozisyon için eksiklerim ne?" |
| **Aktif İş Arayanlar** | Çok sayıda ilana başvuran kişiler | "Hangi ilanlara odaklanmalıyım?" |

### Birincil Persona
**İsim:** Ayşe, 26 yaşında
**Meslek:** Endüstri Mühendisi, yüksek lisans öğrencisi
**Durum:** 6 aydır iş arıyor, data analyst veya product pozisyonlarına başvuruyor
**Acısı:** "Başvurduğum onlarca ilandan dönüş alamıyorum. CV'mde bir şey mi eksik, yoksa yanlış ilanlara mı başvuruyorum bilmiyorum."
**Beklentisi:** CV'sinin ilana uyumunu görmek, eksiklerini bilmek, ne yapması gerektiğini anlamak

---

## 3. Değer Önerisi (Value Proposition)

### Kullanıcı İçin
| Değer | Açıklama |
|-------|----------|
| **Zaman Tasarrufu** | Manuel karşılaştırma yerine saniyeler içinde analiz |
| **Objektiflik** | Duygusal değil, veri tabanlı değerlendirme |
| **Aksiyon Odaklı** | Sadece "eksik" demek değil, "ne yap" önerisi sunmak |
| **Ücretsiz & Gizli** | Yerel çalışır, veriler dışarı çıkmaz |

### İş Değeri
- **Başvuru kalitesini artırır** → Doğru ilanlara, hazırlıklı başvuru
- **Beceri geliştirme sürecini yönlendirir** → Hedefli öğrenme planı
- **Kendine güveni artırır** → Uyum skoruyla somut geri bildirim

---

## 4. Minimum Viable Product (MVP) Kapsamı

### MVP'de Var (Aşama 1) ✅
- [x] CV metni girişi (dosya veya elle)
- [x] İş ilanı metni girişi (dosya veya elle)
- [x] Beceri eşleştirme analizi
- [x] Eksik beceri tespiti
- [x] Uyum skoru (yüzde)
- [x] Somut öneriler

### MVP'de Yok (Bilinçli Kapsam Dışı)
- ❌ Web arayüzü (terminal üzerinden çalışır)
- ❌ PDF yükleme (metin formatında girdi)
- ❌ Çoklu ilan karşılaştırma
- ❌ Kullanıcı hesabı / veri saklama
- ❌ İnteraktif diyalog (tek seferlik analiz)

> **MVP Felsefesi:** En az özellikle en çok değeri doğrula. Kullanıcının gerçekten "beceri eşleştirme" isteyip istemediğini test et.

---

## 5. Kullanıcı Akışı (User Flow)

```
Başlat
  │
  ├── CV Girişi
  │     ├── [1] Dosyadan oku
  │     └── [2] Elle yapıştır
  │
  ├── İlan Girişi
  │     ├── [1] Dosyadan oku
  │     └── [2] Elle yapıştır
  │
  ├── ⏳ Analiz (LLM işleme)
  │
  └── 📊 Sonuç Gösterimi
        ├── CV'deki Beceriler
        ├── İlanda Aranan Beceriler
        ├── ✅ Eşleşen Beceriler
        ├── ❌ Eksik Beceriler
        ├── 💡 Öneriler
        └── 📊 Uyum Skoru
```

---

## 6. Başarı Metrikleri (KPI)

### Aşama 1 (MVP) İçin
| Metrik | Hedef | Ölçüm Yöntemi |
|--------|-------|----------------|
| Çalışıyor mu? | Hatasız çalışan sistem | Manuel test |
| Analiz kalitesi | Mantıklı ve tutarlı sonuçlar | Farklı CV-ilan çiftleriyle test |
| Yanıt süresi | < 60 saniye | Terminal çıktısı |

### İlerleyen Aşamalar İçin (Hedef)
| Metrik | Hedef |
|--------|-------|
| Kullanıcı memnuniyeti | Öneriler "yararlı" olarak değerlendirilmeli |
| Geri ziyaret | Kullanıcı farklı ilanlar için tekrar kullanmalı |
| Portföy etkisi | GitHub'da yıldız/fork sayısı |

---

## 7. Ürün Yol Haritası

### Q1 — Temel MVP ✅
Çalışan bir temel sistem. LangChain + Ollama mantığını doğrula.

### Q2 — Agent ve Akıllı Analiz
- Agent yapısı ile interaktif diyalog
- Daha akıllı kariyer önerileri
- "Hangi projeni öne çıkar" gibi bağlamsal tavsiyeler

### Q3 — Ürünleştirme
- Streamlit web arayüzü
- PDF CV yükleme
- Demo yapılabilir profesyonel ürün

---

## 8. Rekabet Analizi

| Özellik | Bu Proje | Jobscan | Resume Worded |
|---------|----------|---------|---------------|
| Fiyat | Ücretsiz | Ücretli | Ücretli |
| Gizlilik | Yerel çalışır | Bulut | Bulut |
| Beceri eşleştirme | ✅ | ✅ | ✅ |
| Somut öneriler | ✅ | Kısmen | ✅ |
| Türkçe destek | ✅ | ❌ | ❌ |
| Açık kaynak | ✅ | ❌ | ❌ |
| Agent / Diyalog | Aşama 2'de | ❌ | ❌ |

### Farklılaştırıcılar
1. **Tamamen yerel** — veri gizliliği garantisi
2. **Türkçe** — Türk iş piyasasına uygun
3. **Açık kaynak** — şeffaf ve öğretilebilir
4. **Agent yapısı** (Aşama 2) — tek seferlik analiz değil, diyalog tabanlı asistan

---

## 9. Riskler ve Azaltma Stratejileri

| Risk | Etki | Olasılık | Azaltma |
|------|------|----------|---------|
| LLM hallüsinasyonu (uydurma beceri) | Yüksek | Orta | Temperature düşük tutuldu (0.3), prompt detaylı yazıldı |
| Yerel model donanım gereksinimi | Orta | Düşük | Llama3 8B hafif model, çoğu bilgisayarda çalışır |
| Tutarsız çıktı formatı | Orta | Orta | Prompt'ta format şablonu verildi, Aşama 2'de structured output eklenecek |
| Kullanıcı ilgisi düşük | Düşük | Düşük | MVP ile hızlı doğrulama, gerçek ihtiyaca odaklanma |
