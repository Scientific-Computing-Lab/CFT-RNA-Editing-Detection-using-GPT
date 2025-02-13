import matplotlib.pyplot as plt
import numpy as np

# Data for thresholds 1%, 5%, 10%, 15%, "15% ONLY", and "15% ONLY 3.5"
categories = ["1%", "5%", "10%", "15%", "15% ONLY", "15% ONLY 3.5"]
accuracy = [0.7748, 0.9193, 0.9616, 0.9084, 0.8955, 0.8486]
precision = [0.9412, 1.0000, 0.9886, 0.9705, 0.9294, 0.9500]
recall = [0.5881, 0.8375, 0.9338, 0.8436, 0.8548, 0.7342]
specificity = [0.9630, 1.0000, 0.9892, 0.9755, 0.9360, 0.9618]
f1_score = [0.7238, 0.9115, 0.9604, 0.9020, 0.8905, 0.8282]

# Bar width and positions
bar_width = 0.13
positions = np.arange(len(categories))

# Create subplots for better organization
fig, ax = plt.subplots(figsize=(14, 7))

# Plot each metric
bars_accuracy = ax.bar(positions - 2 * bar_width, accuracy, width=bar_width, label="Accuracy", color='blue')
bars_precision = ax.bar(positions - bar_width, precision, width=bar_width, label="Precision", color='green')
bars_recall = ax.bar(positions, recall, width=bar_width, label="Recall", color='orange')
bars_specificity = ax.bar(positions + bar_width, specificity, width=bar_width, label="Specificity", color='red')
bars_f1_score = ax.bar(positions + 2 * bar_width, f1_score, width=bar_width, label="F1 Score", color='purple')

# Add labels at the top of each bar
for bars in [bars_accuracy, bars_precision, bars_recall, bars_specificity, bars_f1_score]:
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.4f}', ha='center', va='bottom', fontsize=9)

# Add labels, title, and set axis limits
ax.set_xlabel("Thresholds", fontsize=12)
ax.set_ylabel("Metric Values", fontsize=12)
ax.set_title("Performance Metrics Across Different Thresholds", fontsize=14)
ax.set_xticks(positions)
ax.set_xticklabels(categories)
ax.set_ylim(0.5, 1.05)

# Move legend to the bottom-right corner
ax.legend(bbox_to_anchor=(1.0, 0.0), loc='lower right', fontsize=10)

# Display the chart
plt.tight_layout()
plt.show()
