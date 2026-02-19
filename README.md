# 🧠 ML Concept Visualizer

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=flat-square)](https://ourarash.github.io/ml-concept-visualizer/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#)

> **Interactive visualizations for machine learning, deep learning, and performance-engineering concepts used in lectures.**

**By Arash Saifhashemi**

## 🌐 [View All Visualizations](https://ourarash.github.io/ml-concept-visualizer/)

Browse the full catalog of interactive visualizations on the **[live website](https://ourarash.github.io/ml-concept-visualizer/)** or explore them directly by opening the HTML files in your browser.

## ✨ Features

- 🎯 **Interactive Visualizations** covering ML fundamentals to advanced optimization
- 📱 **Fully Responsive** - works on desktop, tablet, and mobile
- 🎨 **No Installation Required** - runs entirely in your browser
- 📚 **Educational Focus** - designed for teaching and learning
- ⚡ **Real-time Interaction** - adjust parameters and see immediate results

## 📂 Visualization Categories

### 📊 Classical ML & Classification

Traditional machine learning algorithms and evaluation metrics

- Classification Metrics Explorer (Accuracy, Precision, Recall, F1, ROC, PR curves)
- Decision Trees, KNN, Logistic Regression, SVM
- Neural Network Classification
- K-Means & Hierarchical Clustering

### 🧩 CNN Architectures

Convolutional neural networks and deep learning building blocks

- Convolution operations and output formulas
- Pooling strategies (max, average)
- ResNet architecture and bottleneck blocks
- 1×1 convolutions and dimensionality reduction

### 📚 ML Fundamentals

Core concepts essential for understanding modern ML

- Softmax activation function
- Internal covariate shift and batch normalization
- Mathematical foundations

### ⚡ GEMM Optimization

General Matrix Multiply optimization techniques

- Baseline vs. tiled implementations
- Cache cliff analysis
- Cache miss derivations (tiled and non-tiled)
- Interactive tiling visualizers

### 🔥 Kernel Optimization

Data reuse and computational efficiency patterns

- Spatial and temporal reuse
- Data movement optimization
- Loop-nest transformations

### 💾 Cache & Memory Optimization

Understanding the memory hierarchy

- Cache hierarchy concepts
- Memory access patterns
- Performance implications

### 🔄 Dataflow & Architecture

Hardware dataflow patterns for accelerators

- Input-stationary dataflow
- Output-stationary dataflow
- Weight-stationary dataflow
- Weight-stationary accelerator (8 PE parallel)

### 📈 Performance Modeling

Analyzing and predicting system performance

- Roofline model visualization
- Performance bounds and bottlenecks

## 📁 Repository Structure

```
ml-concept-visualizer/
├── index.html                          # Main landing page
├── fundamentals/                       # Core ML concepts
│   ├── softmax-function-visualizer.html
│   ├── internal-covariate-shift-intuition.html
│   └── internal-covariate-shift-batchnorm.html
├── classical-ml-classification/        # Traditional ML algorithms
│   ├── classification-metrics-visualizer.html
│   ├── decision-tree-visualizer.html
│   ├── knn-visualizer.html
│   ├── logistic-regression-visualizer.html
│   ├── svm-classification-visualizer.html
│   ├── neural-network-classification-visualizer.html
│   ├── k-means-clustering-visualizer.html
│   └── hierarchical-clustering-visualizer.html
├── cnn-architectures/                  # Deep learning & CNNs
│   ├── convolution-basics.html
│   ├── pooling-visualizer.html
│   ├── resnet-architecture-visualizer.html
│   └── ...
├── gemm-optimization/                  # Matrix multiplication optimization
│   ├── gemm-tiling-visualizer.html
│   ├── cache-cliff-and-tiling.html
│   └── ...
├── kernel-optimization/                # Kernel-level optimizations
├── cache-optimization/                 # Memory hierarchy
├── dataflow-loop-nests/               # Hardware dataflow patterns
│   ├── input-stationary-dataflow.html
│   ├── output-stationary-dataflow.html
│   ├── weight-stationary-dataflow.html
│   └── weight-stationary-accelerator-8pe-parallel.html
└── performance-modeling/              # Performance analysis
```

## 🚀 Quick Start

### Option 1: View Online (Recommended)

Visit the **[live website](https://ourarash.github.io/ml-concept-visualizer/)** to browse all visualizations.

### Option 2: Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/ourarash/ml-concept-visualizer.git
   cd ml-concept-visualizer
   ```

2. Open any HTML file in your browser:

   ```bash
   # macOS
   open index.html
   
   # Linux
   xdg-open index.html
   
   # Windows
   start index.html
   ```

3. Or serve locally with Python:

   ```bash
   python -m http.server 8000
   # Visit http://localhost:8000
   ```

## 🤝 Contributing

Contributions are welcome! To add a new visualization:

1. **Fork** the repository
2. **Create** your HTML file in the appropriate category folder
3. Follow the **kebab-case** naming convention
4. Ensure the visualization is **standalone** (no external dependencies beyond CDNs)
5. Add a **brief description** comment at the top of the file
6. Update **index.html** to include your new visualization
7. Submit a **pull request**

### Guidelines

- Make visualizations interactive and educational
- Keep code clean and well-commented
- Test across different browsers
- Ensure responsive design for mobile devices

## 📚 References

- Sze, V., Chen, Y.-H., Yang, T.-J., & Emer, J. S. (2020). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. Morgan & Claypool.

## 📄 License

This project is open source and available for educational purposes.

## 🌟 Acknowledgments

Created by **Arash Saifhashemi** for educational purposes in ML/DL and systems optimization courses.

These visualizations were created with assistance from AI tools to accelerate development and enhance educational content.

---

**⭐ Star this repo** if you find it helpful for learning or teaching!

**🔗 Share** with students and educators who might benefit from these visualizations.

For questions or suggestions, please open an issue or reach out!
