# LangGraph-based-chatbot

A graph‑based chatbot built using **LangGraph** and **LangChain** that demonstrates how conversational AI can be modeled as a **stateful, node‑based workflow** instead of a linear chain.

The project showcases explicit control over conversation flow using a directed graph with clear **START → node → node → END** execution.

---

## 🚀 Features

- Graph‑based conversational flow using LangGraph
- Stateful message handling with explicit transitions
- Modular chatbot nodes for extensibility
- Clear execution path with START and END states
- Demonstrates controlled and predictable LLM orchestration

---

## 🧩 Architecture Overview

```text
START
  ↓
chatbot node (LLM invocation)
  ↓
samplenode (custom logic)
  ↓
END
``
