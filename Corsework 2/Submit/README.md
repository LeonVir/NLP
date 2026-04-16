# 텍스트 다중 라벨 분류 시스템 (Multi-Label Text Classification)

## 📋 프로젝트 요약 (Overview)
비정형 텍스트 데이터를 8개의 카테고리로 동시 분류하는 다중 라벨 분류(Multi-label Classification) 파이프라인입니다. 전통적인 시퀀스 모델부터 최신 SOTA(State-of-the-Art) 모델인 **DeBERTa-v2**까지 아키텍처를 점진적으로 고도화하며, **클래스 불균형(Class Imbalance)** 문제와 **학습 리소스 한계**를 엔지니어링적으로 해결하는 데 집중했습니다.

## 🛠 사용 기술 (Tech Stack)
- **Framework:** PyTorch, Hugging Face Transformers
- **Models:** BiLSTM+Attention, RoBERTa-Base, **DeBERTa-v2 (DebertaV2Model)**
- **Optimization:** AMP(Automatic Mixed Precision), **Asymmetric Loss(ASL)**
- **Methodology:** **Seed Ensemble (Seeds: 16, 42, 378)**, Mean Pooling

---

## 💡 모델 아키텍처의 진화 (Model Evolution)

### 1. Baseline: BiLSTM + Attention (`task1`)
- **수치:** Validation F1-Score **0.5845**
- **특징:** GloVe 임베딩 기반의 양방향 LSTM에 **Custom Attention**을 결합하여 문장의 맥락적 중요도를 파악했습니다.

### 2. Transfer Learning: RoBERTa Fine-tuning (`task2`)
- **수치:** Validation F1-Score **0.6253 (Best)**
- **특징:** 사전 학습된 RoBERTa의 지식을 활용하여 문맥 이해도를 높였으며, 본 프로젝트에서 가장 높은 성능을 기록했습니다.

### 3. SOTA Optimization: DeBERTa-v2 Ensemble (`task3`)
- **수치:** Validation F1-Score **0.6142**
- **핵심 기술 (Mean Pooling & Ensemble):** - **Mean Pooling:** `[CLS]` 토큰에만 의존하지 않고 모든 토큰 벡터의 평균을 사용하는 `DebertaMeanPoolingClassifier`를 구현하여 정보 손실을 최소화했습니다.
    - **Seed Ensemble:** 모델의 일반화 성능과 예측 안정성을 높이기 위해 **3개의 서로 다른 시드(16, 42, 378)**로 개별 학습된 모델들의 예측 확률을 결합(Soft Voting)하는 앙상블 전략을 채택했습니다.

---

## 🔥 핵심 엔지니어링 역량 (Key Engineering Features)

### 1. Asymmetric Loss(ASL)를 통한 불균형 해결
다중 라벨 데이터셋의 고질적 문제인 Negative 샘플의 압도적 비중을 해결하기 위해 **Asymmetric Loss**를 도입했습니다. 쉬운 Negative 샘플의 가중치는 낮추고(Down-weighting), 학습이 어려운 Positive 샘플에 집중하게 하여 모델의 편향성을 최소화했습니다.

### 2. PyTorch AMP를 활용한 학습 최적화
Hugging Face의 무거운 모델을 효율적으로 학습시키기 위해 **AMP(Automatic Mixed Precision)** 기술을 적용했습니다. `torch.amp.autocast`와 `GradScaler`를 통해 정확도 손실 없이 메모리 사용량을 절감하고 학습 속도를 획기적으로 개선했습니다.

---

## 📊 성능 분석 및 인사이트 (Insights)

- **결과 비교:** 최신 모델인 DeBERTa-v2(Model 3)보다 RoBERTa(Model 2)의 성능이 더 높게 나타났습니다.
- **분석:** 이는 모델의 파라미터 크기가 커질수록 주어진 데이터 규모에서 **과적합(Overfitting)**이 발생할 가능성이 높음을 시사합니다. 무조건적인 SOTA 모델 채택보다 **데이터 규모에 최적화된 모델 용량(Capacity)을 선택하는 타협점(Trade-off) 찾기**의 중요성을 확인했습니다.