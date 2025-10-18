import os
import argparse
import pandas as pd
import numpy as np
from typing import List, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from tqdm import tqdm

from preprocess import preprocess_text, tokenize
from embeddings import StaticEmbeddings
from models import LRClassifier, build_cnn, build_lstm, build_cnn_lstm


SEED = 42
np.random.seed(SEED)


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Try likely Arabic/English column names
    candidates_text = [
        'Synopsis', 'summary', 'synopsis', 'الملخص', 'ملخص', 'وصف', 'الوصف',
    ]
    candidates_label = [
        'Category', 'label', 'genre', 'category', 'تصنيف', 'تصنيف الفيلم',
    ]
    text_col, label_col = None, None
    for c in candidates_text:
        if c in df.columns:
            text_col = c
            break
    for c in candidates_label:
        if c in df.columns:
            label_col = c
            break
    if text_col is None or label_col is None:
        raise ValueError(f"Could not find text/label columns in dataset. Columns: {df.columns.tolist()}")
    df = df[[text_col, label_col]].rename(columns={text_col: 'text', label_col: 'label'})
    return df


def build_embeddings_columns(df: pd.DataFrame, vector_size: int, max_len: int,
                             emb: StaticEmbeddings) -> pd.DataFrame:
    tokenized: List[List[str]] = [tokenize(t) for t in df['text']]
    # Train models
    emb.train_word2vec(tokenized)
    emb.train_fasttext(tokenized)

    # Aggregate vectors for LR
    w2v_agg = [emb.sentence_to_vector(toks, kind='w2v') for toks in tokenized]
    ft_agg = [emb.sentence_to_vector(toks, kind='ft') for toks in tokenized]

    # Sequence matrices for deep models
    w2v_seq = [emb.tokens_to_sequence_matrix(toks, max_len=max_len, kind='w2v') for toks in tokenized]
    ft_seq = [emb.tokens_to_sequence_matrix(toks, max_len=max_len, kind='ft') for toks in tokenized]

    df = df.copy()
    df['w2v_agg'] = w2v_agg
    df['ft_agg'] = ft_agg
    df['w2v_seq'] = w2v_seq
    df['ft_seq'] = ft_seq
    return df


def run_experiments(train_df: pd.DataFrame, test_df: pd.DataFrame, label_encoder: LabelEncoder,
                    max_len: int, results_dir: str) -> None:
    os.makedirs(results_dir, exist_ok=True)
    num_classes = len(label_encoder.classes_)

    def save_report(name: str, y_true, y_pred):
        report = classification_report(y_true, y_pred, target_names=label_encoder.classes_, digits=4)
        cm = confusion_matrix(y_true, y_pred)
        with open(os.path.join(results_dir, f"{name}_report.txt"), 'w') as f:
            f.write(report)
            f.write("\nConfusion Matrix:\n")
            f.write(np.array2string(cm))

    # Logistic Regression: AraVec (w2v_agg) and FastText (ft_agg)
    lr = LRClassifier()
    lr.fit(np.vstack(train_df['w2v_agg'].values), train_df['y'].values)
    pred = lr.predict(np.vstack(test_df['w2v_agg'].values))
    save_report('LR_AraVec', test_df['y'].values, pred)

    lr = LRClassifier()
    lr.fit(np.vstack(train_df['ft_agg'].values), train_df['y'].values)
    pred = lr.predict(np.vstack(test_df['ft_agg'].values))
    save_report('LR_FastText', test_df['y'].values, pred)

    # Deep models helper
    def train_deep(name: str, X_train, X_test, builder):
        model = builder(input_shape=X_train.shape[1:], num_classes=num_classes)
        model.fit(X_train, train_df['y'].values, epochs=10, batch_size=32, validation_split=0.1, verbose=0)
        y_pred = model.predict(X_test, verbose=0).argmax(axis=1)
        save_report(name, test_df['y'].values, y_pred)
        model.save(os.path.join(results_dir, f"{name}.keras"))

    # CNN: AraVec and FastText
    Xtr = np.stack(train_df['w2v_seq'].values)
    Xte = np.stack(test_df['w2v_seq'].values)
    train_deep('CNN_AraVec', Xtr, Xte, build_cnn)

    Xtr = np.stack(train_df['ft_seq'].values)
    Xte = np.stack(test_df['ft_seq'].values)
    train_deep('CNN_FastText', Xtr, Xte, build_cnn)

    # LSTM: AraVec and FastText
    Xtr = np.stack(train_df['w2v_seq'].values)
    Xte = np.stack(test_df['w2v_seq'].values)
    train_deep('LSTM_AraVec', Xtr, Xte, build_lstm)

    Xtr = np.stack(train_df['ft_seq'].values)
    Xte = np.stack(test_df['ft_seq'].values)
    train_deep('LSTM_FastText', Xtr, Xte, build_lstm)

    # CNN+LSTM Hybrid
    Xtr = np.stack(train_df['w2v_seq'].values)
    Xte = np.stack(test_df['w2v_seq'].values)
    train_deep('Hybrid_AraVec', Xtr, Xte, build_cnn_lstm)

    Xtr = np.stack(train_df['ft_seq'].values)
    Xte = np.stack(test_df['ft_seq'].values)
    train_deep('Hybrid_FastText', Xtr, Xte, build_cnn_lstm)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, required=False, default='data/movies.csv')
    parser.add_argument('--max_len', type=int, default=150)
    parser.add_argument('--vector_size', type=int, default=300)
    parser.add_argument('--test_size', type=float, default=0.2)
    parser.add_argument('--results', type=str, default='outputs')
    args = parser.parse_args()

    df = load_dataset(args.data)
    # Preprocess
    df['text'] = df['text'].astype(str).map(lambda t: preprocess_text(t))

    # Encode labels
    le = LabelEncoder()
    df['y'] = le.fit_transform(df['label'])

    # Train/test split stratified
    train_df, test_df = train_test_split(df, test_size=args.test_size, random_state=SEED, stratify=df['y'])

    # Build embeddings columns
    emb = StaticEmbeddings(vector_size=args.vector_size)
    train_df = build_embeddings_columns(train_df, args.vector_size, args.max_len, emb)
    # For test, reuse trained models inside emb
    tokenized_test: List[List[str]] = [t.split() for t in test_df['text']]
    test_df = test_df.copy()
    test_df['w2v_agg'] = [emb.sentence_to_vector(toks, kind='w2v') for toks in tokenized_test]
    test_df['ft_agg'] = [emb.sentence_to_vector(toks, kind='ft') for toks in tokenized_test]
    test_df['w2v_seq'] = [emb.tokens_to_sequence_matrix(toks, args.max_len, kind='w2v') for toks in tokenized_test]
    test_df['ft_seq'] = [emb.tokens_to_sequence_matrix(toks, args.max_len, kind='ft') for toks in tokenized_test]

    # Run experiments
    run_experiments(train_df, test_df, le, args.max_len, args.results)

    # Save embeddings for reuse (KeyedVectors)
    try:
        emb.save_kv(args.results, kind='w2v')
        emb.save_kv(args.results, kind='ft')
    except Exception:
        pass

    # Save label encoder
    os.makedirs(args.results, exist_ok=True)
    le_path = os.path.join(args.results, 'label_classes.txt')
    with open(le_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(le.classes_.tolist()))


if __name__ == '__main__':
    main()
