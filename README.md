# Capstone_Working_Demo
# Real College KG Project

## Overview
This repository contains a Knowledge Graph implementation designed for college-related data. It leverages Large Language Models (LLMs) to interact with and query the graph structure effectively.

## Prerequisites & Setup

### 1. Groq API Key
To run this project, you need an API key from Groq.

1.  Visit the [Groq Cloud Console](https://console.groq.com/).
2.  Create an account or log in.
3.  Generate a new API Key.

### 2. Configuration
Once you have your key, you must set it in your environment or configuration. The project looks for the key using the following code:

```python
api_key = os.environ.get("GROQ_API_KEY", "")
