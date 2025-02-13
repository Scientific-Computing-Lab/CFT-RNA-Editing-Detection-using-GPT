import matplotlib.pyplot as plt
import numpy as np

# Data for thresholds 1%, 5%, 10%, 15%, "15% ONLY", and "15% ONLY 3.5"
categories = ["1%", "5%", "10%", "15%", "15% ONLY", "15% ONLY 3.5"]
accuracy = [0.7428,0.7655,0.7753,0.7872,0.7092,0.7154]
precision = [0.8818,0.8044,0.8086,0.8151,0.7326,0.7427]
recall = [0.7248,0.7946,0.7444,0.7358,0.6468,0.6519]
specificity = [0.7832,0.7241,0.8089,0.8373,0.7699,0.7778]
f1_score = [0.7956,0.7994,0.7751,0.7735,0.6871,0.6944]

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
