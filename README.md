# YouTube Live Chat Moderator Pipeline

## Overview

This repository contains a real-time data processing pipeline to moderate live chat comments on YouTube videos. The pipeline scrapes live chat data, classifies the comments as either 'toxic' or 'non-toxic', and stores the information in a PostgreSQL database for easy retrieval and analysis. This is achieved using various Python libraries and adhering to MLOps best practices.

## Features

- Real-time scraping of YouTube live chat data from multiple videos
- Text classification of live chat comments using BERT-based models
- Storing processed data in PostgreSQL
- MLOps-based design for scalability and maintainability

## Technologies Used

- YouTube Data API
- Python Requests Library
- Transformers Library for NLP
- PostgreSQL
- Docker & Kubernetes
- Prometheus & Grafana

## System Design

- **High-Level Design (HLD)**: https://github.com/bozkuya/Toxic_Comment_Classifier/blob/main/System%20Design%20Task.pdf
- **Low-Level Design (LLD)**: [Link to LLD Document](https://github.com/bozkuya/Toxic_Comment_Classifier/blob/main/System%20Design%20Task.pdf)

## Installation and Setup

### Requirements

- Python 3
- PostgreSQL Database
- YouTube API Key

### Steps

Clone the repository
-- git clone https://github.com/bozkuya/Toxic_Comment_Classifier.git
