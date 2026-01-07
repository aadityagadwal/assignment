Task 1 – Rating Prediction via Prompting

--Objective

The goal of this task is to classify Yelp reviews into 1–5 star ratings using Large Language Models (LLMs), returning structured JSON output. The task focuses on prompt design, structured output reliability, and comparative evaluation across different prompting strategies.

--Dataset

The Yelp Reviews dataset was sourced from Kaggle.
To ensure efficiency and stay within free-tier LLM rate limits, a representative subset of reviews was sampled using a fixed random seed.

Total reviews evaluated: 31

Total prompt–review evaluations: 93 (31 reviews × 3 prompts)

Sampling was performed consistently across all prompt variants to ensure a fair comparison.

--Prompting Approaches

Three distinct prompting strategies were designed and evaluated.

1. Baseline Prompt

Description:
A minimal instruction prompt that directly asks the model to predict a star rating and return structured JSON.

Rationale:
This serves as a reference point to understand how the model performs with minimal guidance.

Observation:
While JSON validity was high, accuracy was limited due to the lack of explicit guidance or reasoning structure.

2. Rubric-Based Prompt

Description:
A prompt that provides explicit rating criteria (e.g., what constitutes 1–5 stars) and asks the model to classify the review accordingly.

Rationale:
The intent was to reduce ambiguity by enforcing a consistent interpretation of star ratings.

Observation:
Despite clear rules, performance degraded on nuanced or mixed-sentiment reviews, suggesting that rigid rubrics can reduce flexibility in subjective classification tasks.

3. Reason-Then-Classify Prompt

Description:
A prompt that encourages the model to internally reason about sentiment and review content before producing the final star rating, while still returning only structured JSON.

Rationale:
Encouraging intermediate reasoning often improves alignment with human judgment for subjective tasks.

Observation:
This approach achieved the highest accuracy while maintaining perfect JSON validity, demonstrating the benefit of structured reasoning.

--Evaluation Methodology

Each prompt was evaluated using the following metrics:

Accuracy: Exact match between predicted and actual star ratings

JSON Validity Rate: Percentage of responses that conformed to the required JSON schema

Reliability & Consistency: Stability of structured output across runs

All prompts were evaluated on the same sampled dataset.

--RESULTS:

| Prompt Variant       | Accuracy | JSON Validity Rate |
| -------------------- | -------- | ------------------ |
| Baseline             | 0.23     | 1.00               |
| Rubric-Based         | 0.16     | 1.00               |
| Reason-Then-Classify | 0.45     | 1.00               |

--Discussion & Trade-offs

The baseline prompt provides a simple and reliable starting point but lacks sufficient guidance for nuanced sentiment interpretation.
The rubric-based approach, while structured, proved too rigid for subjective reviews with mixed signals.

The reason-then-classify strategy consistently outperformed other approaches, highlighting the importance of allowing the model to reason before classification. This comes at the cost of slightly increased prompt complexity but yields significantly better alignment with human ratings.

Overall, the results demonstrate a clear trade-off between simplicity, rigidity, and reasoning-driven performance.

--LLM Usage

Multiple LLM backends were explored during development. Due to free-tier rate limits, final evaluation was conducted using a stable LLM backend capable of handling batch evaluation efficiently. The evaluation pipeline is backend-agnostic and can be scaled to larger datasets with higher-throughput access.
