# rag_test
- python=3.13.5
- ollama

📈 Thai OppDay Summarizer — Powered by LLMs
Welcome to Thai OppDay Summarizer, an open-source project that automatically summarizes Opportunity Day (OppDay) presentations of Thai stocks by extracting insights from YouTube subtitles.
No more sifting through hours of investor talks — get crisp, LLM-generated insights in seconds.

🚀 What is Opportunity Day?
In Thailand, listed companies present quarterly performance updates to investors via Opportunity Day. These presentations, often hours long, are packed with valuable information — but staying updated is time-consuming.

🎯 What this project does
📥 Fetch Subtitles
Grab Thai (or English) subtitles directly from YouTube OppDay videos.

🧹 Clean & Chunk Text
Preprocess raw subtitles — remove timestamps, merge lines, handle colloquial Thai or mixed languages.

🤖 Summarize with LLM
Use a large language model (LLM) — OpenAI GPT, LLaMA, or your custom fine-tuned model — to generate a short, structured summary:

Key financial highlights

Management outlook

Notable Q&A insights

Risks & opportunities

🗂️ Output
Deliver summaries in your preferred format: markdown, PDF, CSV, or push directly to Notion, Slack, or a Telegram channel.

