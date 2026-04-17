# Word Similarity Engine (단어 의미 유사도 측정 시스템)

---

## 📋 프로젝트 요약 (Overview)
WikiText-103 대규모 코퍼스를 활용하여, 두 단어 간의 의미적 유사도를 계산하는 NLP 파이프라인입니다. 본 프로젝트는 단어의 문맥과 철자 특징을 모두 포착하기 위해 **Sparse Representation(TF-IDF 하이브리드)과 Dense Representation(FastText) 두 가지 모델을 개발하고 성능을 비교**했습니다.

---

## 🛠 사용 기술 (Tech Stack)
- **Language:** Python
- **NLP (Sparse):** Scikit-learn (TF-IDF, Character N-gram), SciPy
- **NLP (Dense):** Gensim (FastText, Phraser), NLTK
- **Optimization:** In-Memory Caching, Multiprocessing

---

## 💡 핵심 엔지니어링 역량 (Key Engineering Features)

### Model 1: Hybrid Vector (TF-IDF + N-gram) - `CW1_task1`
- **OOV(미등록 단어) 완벽 대응:** 학습 데이터에 없는 미등록 단어(OOV)가 입력될 경우 발생하는 오류를 방지하기 위해 **Character N-gram Vectorizer**를 도입, 철자 기반 추론을 수행했습니다.
- **메모리 최적화:** `_known_vector_cache` 딕셔너리를 활용해 반복 연산을 Caching 하여 대규모 테스트셋 추론 속도를 최적화했습니다.

### Model 2: FastText & Bigram Phraser - `CW1_task2`
- **Subword Information 활용:** Gensim의 FastText 알고리즘을 도입하여 단어의 내부 구조(n-gram)를 학습, 희소성(Sparsity) 문제를 해결하고 OOV 추론 정확도를 높였습니다.
- **Multi-word 처리 (Bigram Phraser):** 'New York'과 같은 복합어를 쪼개지 않고 하나의 토큰으로 묶어 학습하는 `gensim.models.phrases` 파이프라인을 구축하여 문맥 파악 능력을 개선했습니다.
- **병렬 처리(Multiprocessing):** CPU 코어 수 기반의 병렬 처리를 적용하여 대용량 코퍼스의 모델 학습(Training) 시간을 대폭 단축했습니다.

---

## 📊 결과 및 비교 (Results & Insights)
- **성능 평가:** FastText 기반의 Model 2가 69.9%의 정확도(Accuracy)를 기록하여, TF-IDF 하이브리드 기반의 Model 1(68.0%) 대비 향상된 성능을 보였습니다. 
- **엔지니어링 인사이트 (Trade-off):** Model 2가 문맥 파악과 OOV 처리에 더 뛰어난 성능을 보였으나, 모델 학습 및 검증에 소요되는 연산 시간(Time Complexity)은 Model 1보다 크게 증가했습니다. 이를 통해 실제 서비스 적용 시 **'추론 정확도'와 '컴퓨팅 리소스 비용' 간의 트레이드오프(Trade-off)를 고려한 아키텍처 선택이 중요함**을 확인했습니다.