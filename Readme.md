# AI Agent Suite — README

A compact README for an AI agent suite composed of three parts: **ReAct Agent**, **CrewaI Agent**, and **Langraph Agent**. Keep this repository minimal and usable — each component is a small Python module that can be extended independently.

---

# Overview

This project bundles three cooperating agent types:

* **ReAct Agent** — a reasoning-and-acting loop that calls local tools (e.g., `get_summary`, `addition`) and feeds observations back to the model.
* **CrewaI Agent** — a lightweight orchestrator for multi-step workflows and tool coordination (task routing, retries, simple caching).
* **Langraph Agent** — a graph-based context manager that stores and queries conversation/state nodes (useful for longer context, retrieval, and structured memory).

Each agent is designed to be simple to run and easy to extend.

---


