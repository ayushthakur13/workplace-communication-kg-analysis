# Knowledge Graph Construction and Computational Analysis of Workplace Communication using the Enron Email Corpus

## Project Overview

This project analyzes workplace communication patterns using the Enron Email Corpus to extract organizational insights and construct a communication-based Knowledge Graph.

The study integrates Natural Language Processing (NLP), network analysis, and machine learning to model:

- Communication structure
- Work culture indicators
- Performance-related communication signals
- Bias patterns
- Attrition / exit communication behavior

The project emphasizes structured communication modeling and comparative evaluation of ML, Deep Learning, and LLM approaches.

## Dataset

### Enron Email Corpus (Klimt & Yang, 2004)

A publicly available corporate email dataset widely used in NLP and network analysis research.

- ~500,000 emails
- ~150 employees
- Includes sender, recipients, timestamp, subject, and email body
- Stored at: `data/raw/enron_emails.csv`

## Core Components

### 1. Data Preprocessing

- Parse sender, recipients, timestamp, subject, body
- Remove signatures and reply chains
- Normalize text
- Perform tokenization, POS tagging, and NER

### 2. Communication Feature Extraction

- Email frequency per employee
- Response time estimation
- Communication intensity metrics
- Temporal communication patterns

### 3. Knowledge Graph Construction

- **Nodes**: Employees
- **Edges**: Email interactions
- **Edge weights**: Communication frequency
- **Graph Metrics**:
  - Degree centrality
  - Betweenness centrality
  - Community detection

### 4. Model Comparison

#### Machine Learning
- Logistic Regression
- Support Vector Machine (SVM)

#### Deep Learning
- BiLSTM
- BERT (HuggingFace Transformers)

#### LLM Baseline
- Zero-shot intent classification

#### Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-score

## Project Structure

```
workplace-communication-kg/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── preprocessing/
│   ├── models/
│   └── graph/
├── requirements.txt
├── README.md
```

## Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate**:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Place dataset at**:
   ```
   data/raw/enron_emails.csv
   ```

## Expected Outcomes

- Structured workplace communication knowledge graph
- Quantitative comparison of ML, DL, and LLM approaches
- Identified communication-based indicators of:
  - Work culture
  - Performance patterns
  - Bias
  - Attrition signals
- Reproducible research pipeline

## References

- Klimt, B., & Yang, Y. (2004). The Enron Corpus: A New Dataset for Email Classification Research.
- Diesner, J., & Carley, K. (2005). Exploration of communication networks from the Enron email corpus.

## Status

In Development – Data preprocessing and graph construction phase.
