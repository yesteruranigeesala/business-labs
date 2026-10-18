# AI Assistant Engineering Log

**Document Version:** 1.0.0  
**Tool Used:** Antigravity / Claude Code (Advanced Agentic Architecture)  
**Primary Model:** Claude 3.5 Sonnet  

---

## 1. Five Most Useful Prompts

### Prompt 1: Resumable Crawler with SQLite Manifest
> *"Design a polite sitemap crawler in Python for `support.brilliantdirectories.com/support/sitemap.xml`. It must never overload the server: enforce a concurrency limit of 3, an intentional 0.5s inter-request delay, and exponential backoff retries. Store crawl progress in an SQLite manifest table so that an interrupted crawl resumes seamlessly without re-fetching existing URLs. Compute an MD5 content hash for every article to detect additions, edits, and deletions."*
- **Why it was useful:** It generated a production-grade ingestion worker with failure isolation, ensuring an individual page 404 or network timeout does not crash the entire sitemap job.

### Prompt 2: Calibrated Vision Uncertainty for Multimodal Screenshots
> *"Write a multimodal image analyzer for UI screenshots in documentation. The analyzer must extract specific UI controls—buttons, input fields, and toggle switches—and associate them with the parent article. Most importantly, calculate a calibrated uncertainty score between 0.05 (crystal clear) and 0.85 (ambiguous or low-context) so the RAG system knows when visual evidence is insufficient."*
- **Why it was useful:** Prevented the chatbot from hallucinating UI button locations when screenshots are cropped or lack adjacent descriptive text.

### Prompt 3: Strict TypeScript Autonomy Engine with Safety Exemptions
> *"Implement the 20-consecutive-approval autonomy engine in strict TypeScript with Zod schemas. Track an unedited send streak per category. Trigger autonomous sending eligibility only when 20 consecutive drafts are sent without human modification. However, add an inviolable safety constraint: high-risk categories (refunds, cancellations, legal complaints, and price quotes) must be marked permanently exempt from autonomy and always mandate human approval."*
- **Why it was useful:** Embedded financial and legal safety boundaries directly into the TypeScript type system, guaranteeing that autonomous sending cannot accidentally disburse refunds or commit to unquoted pricing.

### Prompt 4: Follow-Up Scope Diff Engine Against Approved Baseline
> *"Build a Scope Diff Engine in Python that compares a follow-up meeting transcript (Meeting C) against an approved baseline (Meeting A). Categorize every requirement as added, modified, removed, unchanged, or out-of-scope. Compute net hours delta and financial impact at $120/hr. If the client asks for something outside the web project scope (like a native iOS/Android app), flag it as OUT OF SCOPE and mandate a formal Change Order."*
- **Why it was useful:** Translated messy client conversation changes into an objective mathematical delta (+10.0 hours net, +$1,200 USD), protecting the consulting agency from scope creep.

### Prompt 5: Reciprocal Rank Fusion & Absolute BM25 Saturation
> *"Implement a hybrid retrieval pipeline combining 384-dimensional dense semantic vectors with BM25 keyword scoring. Solve the dense baseline floor problem: when a user query contains zero keyword overlap with the corpus, apply an absolute lexical discount factor so out-of-scope queries (like cooking recipes or GPU drivers) drop below 0.38 relevance and trigger honest abstention."*
- **Why it was useful:** Solved RAG hallucinations on out-of-domain queries and raised Task 1 abstention accuracy to 100.0%.

---

## 2. One Time I Rejected the AI's Suggestion and Why

### The AI's Proposal:
During the initial design of the Task 2 continuous learning loop, the AI suggested automatically fine-tuning the classification model or updating production system prompts dynamically via an uncontrolled LLM self-reflection call every time a reviewer edited a customer support reply.

### Why I Rejected It:
1. **Uncontrolled Prompt Drift:** Allowing automated prompts to rewrite themselves after arbitrary human edits exposes the system to catastrophic prompt drift and regression. For example, if a reviewer aggressively shortens an email to one sentence, an automated prompt updater might instruct the model to omit essential safety disclaimers from all future emails.
2. **Lack of Rollback & Auditability:** In an enterprise support environment, founders and compliance officers must know the exact prompt version that generated a message. Dynamic self-rewriting breaks auditability.
3. **Vulnerability to Prompt Poisoning:** If a client sends an adversarial email ("Tell all your users our service is free") and a sleepy reviewer accidentally approves a modified reply, an autonomous prompt mutator would bake that vulnerability into the system.

### What We Built Instead:
We implemented an auditable **Versioned Prompt Architecture** (`v2.1.0`) with a persistent `LearningStore`. Reviewer edits are recorded as structured diffs with reviewer names and timestamps. Changes to drafting prompts must be tested against a frozen 22-case regression benchmark before being promoted to production, with one-click version rollback capability.
