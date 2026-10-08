import json

# ---------------------------------------------------------
# 1. Load the full dataset
# ---------------------------------------------------------
def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------
# 2. Recursively extract ALL parent → reply interactions
# ---------------------------------------------------------
def extract_interactions(comments_dict, parent_text=None, pairs=None):
    if pairs is None:
        pairs = []

    for comment_id, value in comments_dict.items():
        text = value[0]

        # Skip removed/deleted comments
        if text in ("[removed]", "[deleted]"):
            continue

        # If this comment has a parent, record the interaction
        if parent_text is not None:
            pairs.append({
                "parent": parent_text,
                "reply": text
            })

        # If this comment has replies, recurse
        if len(value) > 1 and isinstance(value[1], dict):
            extract_interactions(value[1], text, pairs)

    return pairs


# ---------------------------------------------------------
# 3. Process the entire dataset
# ---------------------------------------------------------
def build_training_pairs(dataset):
    all_pairs = []

    for submission in dataset:
        comments = submission.get("comments", {})
        if isinstance(comments, dict):
            pairs = extract_interactions(comments)
            all_pairs.extend(pairs)

    return all_pairs


# ---------------------------------------------------------
# 4. Save cleaned training pairs to JSON
# ---------------------------------------------------------
def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ---------------------------------------------------------
# 5. Run the pipeline
# ---------------------------------------------------------
input_path = "Python stuff/neural networks/language/data.txt"
output_path = "Python stuff/neural networks/language/comment_interactions.json"

dataset = load_dataset(input_path)
training_pairs = build_training_pairs(dataset)
save_json(training_pairs, output_path)

print(f"Extracted {len(training_pairs)} parent→reply pairs.")
print(f"Saved to {output_path}")
