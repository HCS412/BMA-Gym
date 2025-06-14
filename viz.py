# viz.py

import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")

def plot_learning_curve(log_dir, output_path):
    """
    Plot model accuracy or loss from training logs.
    Assumes JSON logs with 'step' and 'accuracy' or 'loss'.
    """
    records = []
    for fname in os.listdir(log_dir):
        if fname.endswith(".json"):
            with open(os.path.join(log_dir, fname)) as f:
                for line in f:
                    data = json.loads(line)
                    records.append(data)

    df = pd.DataFrame(records)
    if 'step' not in df.columns:
        print("Missing 'step' in logs")
        return

    plt.figure(figsize=(10, 6))
    if 'accuracy' in df.columns:
        sns.lineplot(x='step', y='accuracy', data=df, label='Accuracy')
    if 'loss' in df.columns:
        sns.lineplot(x='step', y='loss', data=df, label='Loss')
    plt.title("Training Curve")
    plt.xlabel("Step")
    plt.ylabel("Metric")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_bar(values, labels, title, ylabel, output_path):
    plt.figure(figsize=(8, 6))
    sns.barplot(x=labels, y=values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_accuracy_vs_clones(clone_counts, accuracies, output_path):
    plt.figure(figsize=(8, 5))
    sns.lineplot(x=clone_counts, y=accuracies, marker='o')
    plt.title("Accuracy vs. Clone Count")
    plt.xlabel("Number of Clones (N)")
    plt.ylabel("Accuracy (%)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_merge_rollback(merge_stats, output_path):
    df = pd.DataFrame(merge_stats)
    df['step'] = range(len(df))
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='step', y='merge_rate', data=df, label='Merge Rate')
    sns.lineplot(x='step', y='rollback_rate', data=df, label='Rollback Rate')
    plt.title("Merge vs. Rollback Trends")
    plt.xlabel("Step")
    plt.ylabel("Rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == '__main__':
    # Example usage:
    plot_learning_curve("logs", "outputs/learning_curve.png")
    plot_bar([64.2, 68.4], ["Logic Grid", "Symbol Swap"], "Final Accuracy", "Accuracy (%)", "outputs/final_accuracy.png")
    plot_accuracy_vs_clones([64, 128, 256, 512], [60.1, 63.7, 68.4, 68.6], "outputs/accuracy_vs_clones.png")
    plot_merge_rollback([
        {"merge_rate": 0.8, "rollback_rate": 0.1},
        {"merge_rate": 0.76, "rollback_rate": 0.12},
        {"merge_rate": 0.74, "rollback_rate": 0.14},
    ], "outputs/merge_vs_rollback.png")
