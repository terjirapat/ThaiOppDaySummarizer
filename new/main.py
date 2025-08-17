import os, re, math, time, textwrap
from typing import List, Tuple
import psycopg2
import psycopg2.extras
import ollama
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# ---------- Config ----------
PGHOST     = os.getenv("PGHOST", "localhost")
PGPORT     = int(os.getenv("PGPORT", 5432))
PGDATABASE = os.getenv("PGDATABASE", "ragdb")
PGUSER     = os.getenv("PGUSER", "rag")
PGPASSWORD = os.getenv("PGPASSWORD", "ragpw")

GEN_MODEL = os.getenv("GEN_MODEL", "llama3:8b")
EMB_MODEL = os.getenv("EMB_MODEL", "nomic-embed-text")  # dimension typically 768
TOP_K     = int(os.getenv("TOP_K", 6))
CHUNK_TARGET_CHARS = int(os.getenv("CHUNK_TARGET_CHARS", 1000))  # ~roughly 150–200 tokens
OVERLAP_CHARS      = int(os.getenv("OVERLAP_CHARS", 120))

TABLE_NAME = "youtube_docs"

# ---------- DB ----------
def get_conn():
    return psycopg2.connect(
        host=PGHOST, port=PGPORT, dbname=PGDATABASE, user=PGUSER, password=PGPASSWORD
    )

def init_db(embedding_dim: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        # Create table with dynamic vector dimension
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
              id SERIAL PRIMARY KEY,
              video_id TEXT NOT NULL,
              chunk_id INT NOT NULL,
              content TEXT NOT NULL,
              embedding vector({embedding_dim}) NOT NULL
            );
        """)
        # Fast index (IVFFlat) for cosine distance
        cur.execute(f"CREATE INDEX IF NOT EXISTS {TABLE_NAME}_ivfflat_idx ON {TABLE_NAME} USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);")
        # Helpful default probing
        cur.execute("SET ivfflat.probes = 10;")
        conn.commit()

def clear_video(video_id: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(f"DELETE FROM {TABLE_NAME} WHERE video_id = %s;", (video_id,))
        conn.commit()

def upsert_chunks(video_id: str, chunks: List[str], embeddings: List[List[float]]):
    assert len(chunks) == len(embeddings)
    with get_conn() as conn, conn.cursor() as cur:
        psycopg2.extras.execute_batch(
            cur,
            f"INSERT INTO {TABLE_NAME} (video_id, chunk_id, content, embedding) VALUES (%s, %s, %s, %s);",
            [(video_id, i, chunks[i], embeddings[i]) for i in range(len(chunks))],
            page_size=500
        )
        conn.commit()

def search(query_embedding: List[float], video_id: str, k: int = TOP_K) -> List[Tuple[int, str, float]]:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT chunk_id, content, (embedding <=> %s::vector) AS distance
            FROM {TABLE_NAME}
            WHERE video_id = %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            (query_embedding, video_id, query_embedding, k)
        )
        rows = cur.fetchall()
        return [(r[0], r[1], float(r[2])) for r in rows]

# ---------- Ollama helpers ----------
def embed_texts(texts: List[str]) -> List[List[float]]:
    # Batch embed via Ollama (simple loop; Ollama also supports /embeddings endpoint per text)
    embs = []
    for t in texts:
        r = ollama.embeddings(model=EMB_MODEL, prompt=t)
        embs.append(r["embedding"])
    return embs

def generate(prompt: str, temperature: float = 0.2) -> str:
    resp = ollama.generate(
        model=GEN_MODEL,
        prompt=prompt,
        options={"temperature": temperature}
    )
    return resp["response"]

# ---------- YouTube transcript ----------
def extract_video_id(url_or_id: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{6,})", url_or_id)
    return m.group(1) if m else url_or_id

def get_youtube_transcript(video_id: str) -> str:
    try:
        tlist = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'en-GB', 'auto'])
    except TranscriptsDisabled:
        raise RuntimeError("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise RuntimeError("No transcript found for this video.")
    # Merge with spaces; keep punctuation minimal
    text = " ".join([item["text"].strip() for item in tlist if item["text"].strip()])
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------- Chunking ----------
def smart_split(text: str, target: int = CHUNK_TARGET_CHARS, overlap: int = OVERLAP_CHARS) -> List[str]:
    # Prefer split by sentence boundaries near target sizes
    sents = re.split(r"(?<=[.!?])\s+", text)
    chunks, buf = [], ""
    for s in sents:
        if len(buf) + len(s) + 1 <= target:
            buf += ((" " if buf else "") + s)
        else:
            if buf:
                chunks.append(buf.strip())
            # carry overlap from tail of previous buffer
            carry = buf[-overlap:] if overlap > 0 else ""
            buf = (carry + " " + s).strip() if carry else s
            # if single sentence longer than target, hard split
            while len(buf) > target * 1.5:
                chunks.append(buf[:target].strip())
                buf = (buf[target-overlap:]).strip()
    if buf:
        chunks.append(buf.strip())
    return chunks

# ---------- RAG flow ----------
SYS_SUMMARY = """You are a helpful assistant. When summarizing a YouTube talk, extract the core thesis, key arguments, notable data/quotes, and any actionable takeaways. Use crisp bullets and short paragraphs."""
def build_prompt(question: str, contexts: List[str]) -> str:
    context_block = "\n\n".join([f"[Chunk {i+1}]\n{c}" for i, c in enumerate(contexts)])
    return textwrap.dedent(f"""
    {SYS_SUMMARY}

    Use ONLY the provided context. If insufficient, say so.

    ### Context
    {context_block}

    ### Task
    {question}
    """)

def ingest_video(url_or_id: str) -> Tuple[str, int]:
    video_id = extract_video_id(url_or_id)
    print(f"Fetching transcript for: {video_id}")
    transcript = get_youtube_transcript(video_id)
    chunks = smart_split(transcript)
    print(f"Transcript length: {len(transcript):,} chars; chunks: {len(chunks)}")

    print("Embedding chunks via Ollama...")
    chunk_embs = embed_texts(chunks)
    dim = len(chunk_embs[0])

    print(f"Initializing DB (dim={dim}) and storing chunks...")
    init_db(dim)
    clear_video(video_id)
    upsert_chunks(video_id, chunks, chunk_embs)

    return video_id, len(chunks)

def retrieve(video_id: str, query: str, k: int = TOP_K) -> List[str]:
    q_emb = embed_texts([query])[0]
    results = search(q_emb, video_id, k=k)
    # Return texts ordered by nearest
    return [r[1] for r in results]

def summarize_video(url_or_id: str, style_hint: str = "") -> str:
    video_id, n_chunks = ingest_video(url_or_id)
    base_question = "Write a concise executive summary (150–250 words) followed by 5 key bullet takeaways."
    if style_hint:
        base_question += f" Style hint: {style_hint}"
    contexts = retrieve(video_id, "overall summary of the video", k=TOP_K)
    prompt = build_prompt(base_question, contexts)
    print("Generating summary with Llama 3...")
    return generate(prompt)

# ---------- CLI ----------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RAG on YouTube subtitles using Ollama + pgvector")
    parser.add_argument("--video", required=True, help="YouTube URL or ID")
    parser.add_argument("--ask", help="Ask a question instead of summary")
    parser.add_argument("--k", type=int, default=TOP_K, help="Top-K chunks to retrieve")
    args = parser.parse_args()

    if args.ask:
        vid, _ = ingest_video(args.video)
        ctxs = retrieve(vid, args.ask, k=args.k)
        prompt = build_prompt(args.ask, ctxs)
        print(generate(prompt))
    else:
        print(summarize_video(args.video))
