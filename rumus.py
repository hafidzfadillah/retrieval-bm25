import matplotlib.pyplot as plt

# Define the values for BM25 calculations for three documents
doc_values = {
    "Document 1": {
        "doc_length": 14,
        "bahasa_freq": 0,
        "pemrograman_freq": 2,
        "score": 2.62
    },
    "Document 2": {
        "doc_length": 15,
        "bahasa_freq": 1,
        "pemrograman_freq": 1,
        "score": 4.1034
    },
    "Document 3": {
        "doc_length": 14,
        "bahasa_freq": 0,
        "pemrograman_freq": 0,
        "score": 0.0
    }
}

# Create a visualization for BM25 calculations
fig, ax = plt.subplots(figsize=(12, 4))

# Render each document calculation
for i, (doc, values) in enumerate(doc_values.items()):
    text = f"{doc}:\n" \
           f"BM25 = Σ [ IDF(bahasa) × ( {values['bahasa_freq']} × (1.5 + 1) ) / ({values['bahasa_freq']} + 1.5 × (1 - 0.75 + 0.75 × {values['doc_length']}/14.3334)) ]\n" \
           f"      + IDF(pemrograman) × ( {values['pemrograman_freq']} × (1.5 + 1) ) / ({values['pemrograman_freq']} + 1.5 × (1 - 0.75 + 0.75 × {values['doc_length']}/14.3334))\n" \
           f"Score = {values['score']}"
    ax.text(0.5, 1 - i * 0.35, text, fontsize=10, va='top', ha='center', wrap=True)

ax.axis('off')

# Save the image
image_bm25_filled_path = "files/BM25_filled_formula.png"
plt.savefig(image_bm25_filled_path, bbox_inches='tight', dpi=300)
plt.close(fig)

image_bm25_filled_path



# import matplotlib.pyplot as plt

# # Create a formula image for BM25
# fig, ax = plt.subplots(figsize=(8, 1))
# ax.text(0.5, 0.5, r"$BM25(D, Q) = \sum_{q \in Q} IDF(q) \cdot \frac{f(q, D) \cdot (k_1 + 1)}{f(q, D) + k_1 \cdot (1 - b + b \cdot \frac{|D|}{avgdl})}$",
#         fontsize=15, ha='center', va='center')
# ax.axis('off')

# # Save the image
# image_path = "files/BM25_formula.png"
# plt.savefig(image_path, bbox_inches='tight', dpi=300)
# plt.close(fig)

# # Create a formula image for IDF
# fig, ax = plt.subplots(figsize=(8, 1))
# ax.text(0.5, 0.5, r"$IDF(q) = \log \frac{N - n(q) + 0.5}{n(q) + 0.5} + 1$",
#         fontsize=15, ha='center', va='center')
# ax.axis('off')

# # Save the image
# image_idf_path = "files/IDF_formula.png"
# plt.savefig(image_idf_path, bbox_inches='tight', dpi=300)
# plt.close(fig)

# (image_path, image_idf_path)
