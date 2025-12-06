# Data Quality Checker

A web-based data quality analysis tool built with Python and Flask that provides comprehensive quality metrics for CSV datasets.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📊 Overview

Upload a CSV file through a clean web interface and receive a detailed quality report with a comprehensive scoring system based on industry-standard data quality dimensions.

## ✨ Features

- **Web-based Upload Interface** - Drag-and-drop or click to upload CSV files
- **Comprehensive Quality Scoring** - 6-dimension weighted quality framework:
  - **Completeness (30%)** - Missing value analysis
  - **Uniqueness (20%)** - Duplicate row detection
  - **Validity (20%)** - Data type correctness
  - **Consistency (15%)** - Statistical variation analysis
  - **Accuracy (10%)** - Outlier detection using IQR method
  - **Timeliness (5%)** - Data freshness (placeholder)
- **Visual Reports** - HTML reports with:
  - Overall quality score and rating (Excellent/Good/Fair/Poor)
  - Individual dimension scores with visual cards
  - Detailed tables for missing values, outliers, and column metadata
- **Encoding Support** - Handles UTF-8, Latin-1, and CP1252 encoded files
- **File Size Support** - Up to 100MB CSV files

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Samarth-2003-web/Data-quality-checker.git
cd Data-quality-checker
```

2. Install required packages:
```bash
pip install flask pandas numpy
```

### Running the Application

1. Start the Flask server:
```bash
python web_app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload a CSV file and view the quality report!

## 📁 Project Structure

```
Data-quality-checker/
│
├── web_app.py                      # Flask application (main backend)
├── app.py                          # Command-line version
├── templates/
│   ├── upload.html                 # File upload interface
│   └── report_template.html        # Quality report template
├── uploads/                        # Uploaded files (auto-created)
├── sample_data.csv                 # Sample dataset for testing
└── README.md                       # Project documentation
```

## 🧮 Quality Scoring Formula

```python
Overall Score = (
    Completeness × 0.30 +
    Uniqueness × 0.20 +
    Validity × 0.20 +
    Consistency × 0.15 +
    Accuracy × 0.10 +
    Timeliness × 0.05
)
```

### Score Ratings

- **90-100%** → EXCELLENT (Green)
- **75-89%** → GOOD (Yellow)
- **60-74%** → FAIR (Blue)
- **0-59%** → POOR (Red)

## 📊 Example Output

The tool generates an interactive HTML report showing:

1. **Overview Metrics**
   - Total rows and columns
   - Duplicate count
   - Missing values count

2. **Quality Score Breakdown**
   - Overall weighted score
   - Individual dimension scores
   - Visual quality rating

3. **Detailed Analysis**
   - Missing values per column (count + percentage)
   - Outliers per numeric column (IQR method)
   - Column data types

## 🛠️ Technologies Used

- **Backend**: Python 3.x, Flask
- **Data Processing**: pandas, NumPy
- **Frontend**: HTML5, CSS3 (Jinja2 templates)
- **Statistical Methods**: IQR outlier detection, coefficient of variation

## 📝 Use Cases

- Data quality assessment before analysis
- ETL pipeline validation
- Dataset health monitoring
- Data governance compliance checks
- Pre-processing data exploration

## 🔮 Future Enhancements

- [ ] Support for Excel and Parquet files
- [ ] Advanced validity rules (regex, domain constraints)
- [ ] Date/time column freshness checks
- [ ] User authentication and session management
- [ ] Export reports as PDF
- [ ] Comparison between multiple datasets
- [ ] Cloud deployment (AWS/Azure/GCP)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Samarth**
- GitHub: [@Samarth-2003-web](https://github.com/Samarth-2003-web)

## 🙏 Acknowledgments

Built as a learning project to explore:
- Flask web framework
- Data quality engineering concepts
- Full-stack development practices

---

⭐ **Star this repository** if you find it helpful!
