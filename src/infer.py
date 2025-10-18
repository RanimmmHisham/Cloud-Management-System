import argparse
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from preprocess import preprocess_text
from embeddings import StaticEmbeddings
from tensorflow import keras


def load_label_classes(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def predict_samples(samples, results_dir: str, model_name: str, emb: StaticEmbeddings, max_len: int):
    model_path = os.path.join(results_dir, f"{model_name}.keras")
    model = keras.models.load_model(model_path)

    tokenized = [preprocess_text(s).split() for s in samples]
    X = np.stack([emb.tokens_to_sequence_matrix(t, max_len, kind=('w2v' if 'AraVec' in model_name else 'ft')) for t in tokenized])
    probs = model.predict(X, verbose=0)
    return probs.argmax(axis=1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results', type=str, default='outputs')
    parser.add_argument('--best', type=str, required=True, help='Best model name, e.g., CNN_AraVec')
    parser.add_argument('--max_len', type=int, default=150)
    args = parser.parse_args()

    label_classes = load_label_classes(os.path.join(args.results, 'label_classes.txt'))
    emb = StaticEmbeddings()
    # Embeddings must be trained or loaded; in this simple demo, we cannot reconstruct w2v/ft vocab without retraining.
    # For a real pipeline, save and reload the embedding models. Here we assume a script-level integration where emb is available.
    raise SystemExit("This inference script expects to be run in the same session as training with available embeddings.")


if __name__ == '__main__':
    main()
