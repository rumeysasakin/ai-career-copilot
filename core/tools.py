"""
LangChain tool tanımları — Agent pipeline'ında kullanılır.

Tüm tool'lar @tool dekoratörü ile işaretlenmiştir.
Programatik olarak çağrılır (hibrit yaklaşım).
"""

import re
from langchain_core.tools import tool
from .skills import extract_skills, normalize_skill


@tool
def beceri_cikar(metin: str, kaynak: str) -> str:
    """CV veya iş ilanı metninden teknik becerileri çıkarır.

    Args:
        metin: Analiz edilecek metin
        kaynak: 'cv' veya 'ilan'
    """
    beceriler = extract_skills(metin)
    if not beceriler:
        return f"[{kaynak.upper()}] Bilinen bir beceri bulunamadı."
    return f"[{kaynak.upper()}] Bulunan beceriler ({len(beceriler)}): {', '.join(beceriler)}"


@tool
def karsilastir(cv_skills: str, job_skills: str) -> str:
    """CV ve iş ilanı becerilerini karşılaştırır, eşleşen ve eksik olanları bulur.

    Args:
        cv_skills: CV'den çıkarılan becerilerin virgüllü listesi
        job_skills: İş ilanından çıkarılan becerilerin virgüllü listesi
    """
    cv_set = _parse_skills(cv_skills)
    job_set = _parse_skills(job_skills)

    eslesen = set()
    for cv_b in cv_set:
        for job_b in job_set:
            if cv_b == job_b:
                eslesen.add(job_b)
            elif cv_b in job_b or job_b in cv_b:
                eslesen.add(job_b)
            elif len(cv_b) > 2 and len(job_b) > 2:
                cv_words = set(cv_b.split())
                job_words = set(job_b.split())
                ortak = cv_words & job_words
                if ortak and any(len(w) > 2 for w in ortak):
                    eslesen.add(job_b)

    eksik = job_set - eslesen

    return (
        f"Eslesen beceriler ({len(eslesen)}): {', '.join(sorted(eslesen)) if eslesen else 'Yok'}\n"
        f"Eksik beceriler ({len(eksik)}): {', '.join(sorted(eksik)) if eksik else 'Yok'}\n"
        f"Toplam aranan: {len(job_set)}, Eslesen: {len(eslesen)}"
    )


@tool
def skor_hesapla(eslesen: int, toplam: int) -> str:
    """Uyum skorunu hesaplar (eşleşen / toplam × 100).

    Args:
        eslesen: Eşleşen beceri sayısı
        toplam: Toplam aranan beceri sayısı
    """
    if toplam == 0:
        return "Skor hesaplanamadı — toplam 0."

    skor = round((eslesen / toplam) * 100)

    if skor >= 80:
        yorum = "Mükemmel uyum! Bu ilana güvenle başvurabilirsiniz."
    elif skor >= 60:
        yorum = "İyi uyum. Birkaç eksik beceriyi hızlıca kapatabilirsiniz."
    elif skor >= 40:
        yorum = "Orta uyum. Eksik becerilere odaklanmanız gerekiyor."
    else:
        yorum = "Düşük uyum. Bu ilan için ciddi hazırlık gerekebilir."

    return f"Uyum Skoru: %{skor} — {yorum}"


# Beceriye özel, portföy odaklı somut öneriler
ONERI_HARITASI = {
    "docker": (
        "Mevcut projelerinizden birini Dockerfile ile konteynerize edin. "
        "docker-compose ile multi-service ortam kurun (ör: Django + PostgreSQL + Redis). "
        "GitHub'a 'dockerized-app' reposu olarak yükleyin."
    ),
    "kubernetes": (
        "Minikube ile yerel K8s cluster kurun. Docker imajınızı pod olarak deploy edin. "
        "Deployment + Service YAML'larını GitHub'a ekleyin."
    ),
    "fastapi": (
        "FastAPI ile küçük bir REST API projesi oluşturun (ör: URL shortener). "
        "Swagger dokümanı otomatik oluşsun, async endpoint yazın. GitHub'a yükleyin."
    ),
    "ci/cd": (
        "GitHub Actions ile mevcut projenize test + lint pipeline'ı ekleyin. "
        ".github/workflows/ci.yml dosyası oluşturup push'ta pytest çalıştırın."
    ),
    "jenkins": (
        "Jenkins'i Docker ile kurun. GitHub reponuza bağlı Pipeline (Jenkinsfile) yazın. "
        "Build → Test → Deploy aşamalarını tanımlayın."
    ),
    "redis": (
        "Django/Flask projenize redis cache ekleyin (django-redis). "
        "Session storage veya API response caching implementasyonu yapın."
    ),
    "celery": (
        "Django projenize Celery + Redis entegrasyonu yapın. "
        "Email gönderimi gibi uzun süren işlemi asenkron task'a çevirin."
    ),
    "rabbitmq": (
        "RabbitMQ'yu Docker ile kurun. Producer-consumer örneği yazın. "
        "Celery backend olarak entegre edin."
    ),
    "pytest": (
        "Mevcut projenizin en önemli 3 fonksiyonu için unit test yazın. "
        "pytest-cov ile coverage raporu oluşturun. CI pipeline'a entegre edin."
    ),
    "microservices": (
        "Monolitik projeyi iki servise bölün (ör: auth-service + api-service). "
        "Docker Compose ile orkestre edin. Servisler arası REST iletişimi kurun."
    ),
    "postgresql": (
        "PostgreSQL'de index, JOIN ve EXPLAIN ANALYZE komutlarını deneyin. "
        "Django ORM sorgularının SQL karşılıklarını inceleyin."
    ),
    "mysql": (
        "MySQL Workbench ile sorgu pratiği yapın. "
        "PostgreSQL biliyorsanız syntax farklılıklarını öğrenin."
    ),
    "aws": (
        "AWS Free Tier ile EC2 + S3 + RDS kullanarak web uygulaması deploy edin. "
        "Lambda ile serverless fonksiyon yazın. Altyapı dokümanını GitHub'a ekleyin."
    ),
    "azure": "Azure App Service ile Python web uygulaması deploy edin. Azure DevOps pipeline'ı kurun.",
    "gcp": "Google Cloud Run ile konteyner deploy edin. BigQuery ile veri analizi deneyin.",
    "react": (
        "Portfolio sitesi veya dashboard projesi oluşturun. "
        "Props, state, useEffect ve API entegrasyonu pratiği yapın."
    ),
    "vue": "Vue CLI ile component bazlı proje oluşturun. Reactivity ve Pinia öğrenin.",
    "angular": "Angular CLI ile proje oluşturup component, service ve routing öğrenin.",
    "machine learning": (
        "scikit-learn ile sınıflandırma projesi yapın (ör: titanic). "
        "Kaggle'da beginner yarışmalarına katılın. Sonuçları GitHub'da paylaşın."
    ),
    "deep learning": (
        "PyTorch veya TensorFlow ile MNIST el yazısı tanıma projesi yapın. "
        "Training loop, loss function ve evaluation metriklerini öğrenin."
    ),
    "nlp": (
        "Hugging Face transformers ile sentiment analizi yapın. "
        "Kendi verinizle fine-tuning deneyin. Sonuçları GitHub'da paylaşın."
    ),
    "langchain": (
        "Bu projeyi referans alın! RAG (Retrieval Augmented Generation) örneği yapın. "
        "LangChain dokümanındaki quickstart'ı tamamlayın."
    ),
    "graphql": "Strawberry/Graphene ile GraphQL API oluşturup REST ile kıyaslayın.",
    "kafka": "Docker ile Kafka cluster kurun. Python confluent-kafka ile producer-consumer yazın.",
    "elasticsearch": "Docker ile Elasticsearch kurun. Python client ile index ve arama yapın.",
    "selenium": "Selenium ile web sitesi otomatik test scripti yazın. Page Object Pattern öğrenin.",
    "power bi": (
        "Örnek veri seti ile interaktif dashboard oluşturun. "
        "DAX formülleri ve ilişki modelleme öğrenin. Dashboard'u portfolyonuza ekleyin."
    ),
    "tableau": "Tableau Public ile ücretsiz dashboard oluşturup yayınlayın.",
    "jira": "Kendi projeniz için Jira board oluşturun. Sprint planlama pratiği yapın.",
    "agile": "Scrum Guide'ı okuyun. Projelerinizde 1 haftalık sprint döngüleri uygulayın.",
    "scrum": "Daily standup, sprint review ve retrospective formatlarını uygulayın.",
    "git": (
        "Git Flow veya trunk-based branching öğrenin. "
        "Interactive rebase ve cherry-pick komutlarını deneyin."
    ),
    "linux": (
        "WSL veya VM ile Linux komut satırını günlük işinizde kullanın. "
        "Bash scripting ile otomasyon yapın."
    ),
    "rest api": "OpenAPI/Swagger spec yazmayı öğrenin. Postman ile API test koleksiyonu oluşturun.",
    "sql": "LeetCode/HackerRank'te SQL soruları çözün. Window functions ve CTE'leri öğrenin.",
    "nosql": "MongoDB Atlas free tier ile doküman DB deneyin. Aggregation pipeline öğrenin.",
    "mongodb": "MongoDB Atlas ile koleksiyon oluşturun. Aggregation pipeline ve index öğrenin.",
}


@tool
def oneri_uret(eksik_beceriler: str, mevcut_beceriler: str) -> str:
    """Eksik becerilere göre somut, portföy odaklı kariyer önerileri üretir.

    Args:
        eksik_beceriler: Virgüllü eksik beceri listesi
        mevcut_beceriler: Virgüllü mevcut beceri listesi
    """
    eksik_list = [b.strip().lower() for b in eksik_beceriler.split(",") if b.strip()]
    mevcut_list = [b.strip().lower() for b in mevcut_beceriler.split(",") if b.strip()]

    oneriler = []
    for beceri in eksik_list:
        norm = normalize_skill(beceri)
        if norm in ONERI_HARITASI:
            oneriler.append(f"- **{beceri}**: {ONERI_HARITASI[norm]}")
        else:
            oneriler.append(
                f"- **{beceri}**: Resmi dokümanı okuyun, küçük bir pratik proje yapın "
                f"ve GitHub'a yükleyin."
            )

    if not oneriler:
        oneriler.append("Tüm beceriler mevcut! Pratik projelerle pekiştirin.")

    return (
        f"Mevcut beceriler ({len(mevcut_list)}): {', '.join(mevcut_list)}\n"
        f"Eksik beceriler ({len(eksik_list)}): {', '.join(eksik_list)}\n\n"
        f"Somut Öneriler:\n" + "\n".join(oneriler)
    )


# Tool listesi — Agent pipeline ve dışarıdan erişim için
ALL_TOOLS = [beceri_cikar, karsilastir, skor_hesapla, oneri_uret]


def _parse_skills(beceri_str: str) -> set:
    """Virgüllü beceri stringini normalize edilmiş set'e çevirir."""
    parcalar = re.split(r'[,\n\-•]', beceri_str)
    result = set()
    for p in parcalar:
        cleaned = p.strip().lower()
        if cleaned and len(cleaned) > 1:
            result.add(normalize_skill(cleaned))
    return result
