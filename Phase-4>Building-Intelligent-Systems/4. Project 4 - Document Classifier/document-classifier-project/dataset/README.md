# Dataset

Place training images into one folder per document class:

```text
dataset/
├── resume/
├── invoice/
├── certificate/
└── id/
```

The folder names become the model labels.

Inspect the dataset before training. In particular, look for:

- class imbalance
- duplicate images
- unreadable images
- inconsistent image quality
- near-duplicate images across splits
- classes that are visually difficult to distinguish

Do not put test images in the dataset without understanding how the training
script splits the data.
