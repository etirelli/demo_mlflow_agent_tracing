import logging

from datasets import Dataset, load_dataset
from demo_mlflow_agent_tracing.constants import DB_PATH
from tqdm import tqdm

logger = logging.getLogger(__name__)


def accept_row(row: dict[str, str]) -> bool:
    """Decide if the row should be accepted or rejected."""
    # Reject questions that cannot be attributed to a person, e.g. "Did his mother die of pneumonia?"
    reject_patterns = [" he ", " she ", " they ", " him ", " her ", " they ", " his ", " hers ", " theirs "]
    if any(pat in row["question"] for pat in reject_patterns):
        return False

    return True


def main():
    """Load and filter evaluation dataset, then save to JSONL file."""
    # Load the eval dataset
    dataset = "rag-datasets/rag-mini-wikipedia"
    qnas = load_dataset(dataset, "question-answer")["test"]
    logger.info(f"Read {qnas.num_rows} QA pairs from {dataset}")

    # Filter out impossible questions
    keeps = []
    for row in tqdm(qnas, desc="Filtering QA pairs..."):
        if accept_row(row):
            row["dataset"] = dataset
            keeps.append(row)

    # Save keeps to a new dataset
    keeps_ds = Dataset.from_list(keeps)
    logger.info(f"Saving {keeps_ds.num_rows} QA pairs from {dataset}")
    outpath = DB_PATH / "evaluation.jsonl"
    keeps_ds.to_json(outpath)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    main()
