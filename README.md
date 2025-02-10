# CFT-RNA-Editing-Detection-using-GPT

## Overview
RNA editing is a crucial post-transcriptional mechanism that alters RNA sequences, impacting gene regulation and disease. This repository contains code for predicting adenosine-to-inosine (A-to-I) RNA editing sites using GPT-4o-mini with a continual fine-tuning (CFT) strategy.

We introduce a liver-specific dataset, where ADAR1 is the predominant enzyme, and train models progressively on editing thresholds (1%, 5%, 10%, 15%), improving classification accuracy compared to traditional fine-tuning methods.

## 🧬 Methodology
Our approach focuses on improving RNA editing site prediction using transformer-based models, specifically **GPT-4o-mini**, in a **continual fine-tuning (CFT)** paradigm. This methodology allows the model to progressively learn from lower to higher editing thresholds (1%, 5%, 10%, 15%), refining its understanding of RNA editing patterns.

We trained the model using a **liver-specific dataset** derived from GTEx, ensuring minimal interference from non-relevant ADAR isoforms. The training procedure included:

1. **Data Collection & Preprocessing**
   - Extracting double-stranded RNA (dsRNA) structures from Alu elements.
   - Annotating editing levels based on GTEx liver data.
   - Converting RNA secondary structure into ViennaRNA format.

2. **Continual Fine-Tuning Strategy**
   - Initially training on a low-threshold dataset (1%).
   - Gradually increasing thresholds (5%, 10%, 15%) to refine model performance.
   - Ensuring each step retains prior knowledge while learning new distinctions.

3. **Evaluation & Results**
   - Comparison between **static fine-tuning** and **continual fine-tuning**.
   - Assessment of **overlapping vs. non-overlapping threshold binning**.
   - Performance measured via **accuracy, precision, recall, F1-score**.
   - **Figures from the study** (to be included) illustrate the effectiveness of our approach.

