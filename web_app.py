from flask import Flask, render_template, request, send_file
import pandas as pd
import numpy as np
import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No file selected", 400
    
    if not file.filename.endswith('.csv'):
        return "Only CSV files are allowed", 400
    
    # Save uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Load and analyze data with encoding handling
    try:
        data = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        # Try with different encodings
        try:
            data = pd.read_csv(filepath, encoding='latin-1')
        except:
            data = pd.read_csv(filepath, encoding='cp1252')
    
    report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ============================================
    # COMPREHENSIVE QUALITY SCORING SYSTEM
    # ============================================
    
    # 1. COMPLETENESS SCORE (30% weight)
    # Measures: Missing values
    total_cells = len(data) * len(data.columns)
    missing_cells = data.isnull().sum().sum()
    completeness_score = ((total_cells - missing_cells) / total_cells) * 100
    
    # 2. UNIQUENESS SCORE (20% weight)
    # Measures: Duplicate rows
    duplicate_rows = data.duplicated().sum()
    uniqueness_score = max(0, 100 - (duplicate_rows / len(data) * 100))
    
    # 3. VALIDITY SCORE (20% weight)
    # Measures: Data type correctness
    validity_issues = 0
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        # Check for inf/-inf values
        validity_issues += np.isinf(data[col]).sum()
    
    validity_score = max(0, 100 - (validity_issues / total_cells * 1000))
    
    # 4. CONSISTENCY SCORE (15% weight)
    # Measures: Coefficient of variation (standard deviation relative to mean)
    consistency_score = 100
    if len(numeric_cols) > 0:
        cv_scores = []
        for col in numeric_cols:
            if data[col].std() != 0 and data[col].mean() != 0:
                cv = (data[col].std() / abs(data[col].mean())) * 100
                # Penalize high coefficient of variation (>50%)
                cv_scores.append(max(0, 100 - cv))
        consistency_score = np.mean(cv_scores) if cv_scores else 100
    
    # 5. ACCURACY SCORE (10% weight)
    # Measures: Outliers detected using IQR method
    outlier_summary = []
    outlier_count = 0
    
    for col in numeric_cols:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
        outlier_count += len(outliers)
        
        if len(outliers) > 0:
            outlier_summary.append({
                'Column': col,
                'Outlier_Count': len(outliers),
                'Outlier_Percent': f"{(len(outliers)/len(data)*100):.2f}%",
                'Lower_Bound': f"{lower_bound:.2f}",
                'Upper_Bound': f"{upper_bound:.2f}"
            })
    
    accuracy_score = max(0, 100 - (outlier_count / len(data) * 10))
    
    # 6. TIMELINESS SCORE (5% weight)
    # For this demo, assume data is fresh (100%)
    timeliness_score = 100
    
    # ============================================
    # WEIGHTED OVERALL SCORE
    # ============================================
    
    weights = {
        'completeness': 0.30,
        'uniqueness': 0.20,
        'validity': 0.20,
        'consistency': 0.15,
        'accuracy': 0.10,
        'timeliness': 0.05
    }
    
    overall_score = (
        completeness_score * weights['completeness'] +
        uniqueness_score * weights['uniqueness'] +
        validity_score * weights['validity'] +
        consistency_score * weights['consistency'] +
        accuracy_score * weights['accuracy'] +
        timeliness_score * weights['timeliness']
    )
    
    # Missing values report
    missing_values = data.isnull().sum()
    missing_percent = (missing_values / len(data)) * 100
    
    missing_report = pd.DataFrame({
        'Column': missing_values.index,
        'Missing_Count': missing_values.values,
        'Missing_Percent': missing_percent.values
    })
    missing_report = missing_report[missing_report['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
    
    # Score classification
    if overall_score >= 90:
        score_class = 'excellent'
        score_label = 'EXCELLENT'
    elif overall_score >= 75:
        score_class = 'good'
        score_label = 'GOOD'
    elif overall_score >= 60:
        score_class = 'fair'
        score_label = 'FAIR'
    else:
        score_class = 'poor'
        score_label = 'POOR'
    
    return render_template('report_template.html',
                         report_date=report_date,
                         total_rows=f"{len(data):,}",
                         total_columns=len(data.columns),
                         duplicate_count=f"{duplicate_rows:,}",
                         missing_cells=f"{missing_cells:,}",
                         overall_score=f"{overall_score:.1f}",
                         score_label=score_label,
                         completeness_score=f"{completeness_score:.1f}",
                         uniqueness_score=f"{uniqueness_score:.1f}",
                         validity_score=f"{validity_score:.1f}",
                         consistency_score=f"{consistency_score:.1f}",
                         accuracy_score=f"{accuracy_score:.1f}",
                         timeliness_score=f"{timeliness_score:.1f}",
                         score_class=score_class,
                         missing_report_html=missing_report.to_html(index=False) if len(missing_report) > 0 else '<p class="pass">No missing values found</p>',
                         outlier_html=pd.DataFrame(outlier_summary).to_html(index=False) if outlier_summary else '<p class="pass">No outliers detected</p>',
                         column_details_html=data.dtypes.to_frame('Data_Type').to_html())

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
