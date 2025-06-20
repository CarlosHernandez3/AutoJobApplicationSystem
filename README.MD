# 🧠 AutoJobApply: Multi-Agent Job Application System

A modular, LLM-powered multi-agent system that automates reviewing job descriptions, tailoring resumes, generating personalized cover letters, and submitting job applications — all with LangChain orchestration and LLM APIs.

---

## ✨ Project Goal

Build a fully functioning, observable multi-agent system that:
- Ingests job descriptions (scraped)
- Matches job descriptions to your resume
- Tailors your resume and generates a personalized cover letter 
- Applies to the job automatically or logs the application
- Logs all steps and errors for traceability

---

## 🧰 Tech Stack

- **LangChain** (Agents, Chains, Tools, Memory)
- **OpenAI API / Anthropic API**
- **Python**
- **FAISS / Chroma (optional vector search)**
- **Streamlit** (CLI or minimal UI)
- **JSON** (for memory & application tracking)
- **Playwright / Selenium** (optional job application bot)
- **LangSmith**

---

## 🧱 System Architecture (High-Level)

[Job Description Scraper/Loader] ---> 
[Job Review Agent] --->
[Filtered Jobs]--->
[Resume Tailoring Agent]--->
[Cover Letter Writer Agent]--->
[Application Submitter Agent]--->
[Logs / Status / History]

