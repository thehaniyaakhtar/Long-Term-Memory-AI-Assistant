
import csv
import time
from pathlib import Path
from datetime import datetime, timezone

import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer

from app.database.database import SessionLocal
from app.memory.retrieval_service import retrieve_memories


USER_ID = 1
TOP_K = 5

RESULTS_DIR = Path("evaluation/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = RESULTS_DIR / "history.csv"
GRAPH_PATH = RESULTS_DIR / "retrieval_history.png"

model = SentenceTransformer("all-MiniLM-L6-v2")

# Edit these examples to match memories actually saved
# in your PostgreSQL database.
TEST_CASES = [
    {
        "question": "What am I studying?",
        "expected_text": "AIML",
    },
    {
        "question": "What subject am I learning?",
        "expected_text": "machine learning",
    },
]


def evaluate():
    db = SessionLocal()

    hits = 0
    reciprocal_ranks = []
    latencies = []

    try:
        for case in TEST_CASES:
            query_embedding = model.encode(
                case["question"]
            ).tolist()

            start = time.perf_counter()

            memories = retrieve_memories(
                db=db,
                user_id=USER_ID,
                query_embedding=query_embedding,
                limit=TOP_K,
            )

            latencies.append(
                time.perf_counter() - start
            )

            expected = case["expected_text"].lower()

            rank = None

            for position, memory in enumerate(
                memories, start=1
            ):
                if expected in memory.memory_text.lower():
                    rank = position
                    break

            if rank is not None:
                hits += 1
                reciprocal_ranks.append(1 / rank)
            else:
                reciprocal_ranks.append(0)

            print("\nQuestion:", case["question"])
            print("Expected:", case["expected_text"])
            print(
                "Retrieved:",
                [m.memory_text for m in memories]
            )
            print("Correct rank:", rank)

    finally:
        db.close()

    total = len(TEST_CASES)

    if total == 0:
        print("Add test cases before running.")
        return

    recall_at_5 = hits / total
    mrr = sum(reciprocal_ranks) / total
    avg_latency = sum(latencies) / len(latencies)

    timestamp = datetime.now(
        timezone.utc
    ).isoformat(timespec="seconds")

    print("\n--- Evaluation results ---")
    print(f"Recall@{TOP_K}: {recall_at_5:.2%}")
    print(f"MRR: {mrr:.3f}")
    print(f"Average retrieval latency: {avg_latency:.4f}s")

    file_exists = CSV_PATH.exists()

    with CSV_PATH.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "recall_at_5",
                "mrr",
                "avg_latency_seconds",
            ])

        writer.writerow([
            timestamp,
            recall_at_5,
            mrr,
            avg_latency,
        ])

    plot_history()


def plot_history():
    timestamps = []
    recalls = []
    mrrs = []

    with CSV_PATH.open(
        newline="", encoding="utf-8"
    ) as file:
        for row in csv.DictReader(file):
            timestamps.append(row["timestamp"])
            recalls.append(
                float(row["recall_at_5"]) * 100
            )
            mrrs.append(float(row["mrr"]) * 100)

    if not timestamps:
        return

    plt.figure(figsize=(10, 5))
    plt.plot(
        range(1, len(recalls) + 1),
        recalls,
        marker="o",
        label="Recall@5 (%)",
    )
    plt.plot(
        range(1, len(mrrs) + 1),
        mrrs,
        marker="o",
        label="MRR (%)",
    )

    plt.xlabel("Evaluation run")
    plt.ylabel("Score (%)")
    plt.title("Memory Retrieval Quality Over Repeated Evaluations")
    plt.ylim(0, 105)
    plt.xticks(range(1, len(timestamps) + 1))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(GRAPH_PATH)
    plt.close()

    print("\nGraph saved to:", GRAPH_PATH)


if __name__ == "__main__":
    evaluate()
