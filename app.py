# Libraries
import pandas as pd
import numpy as np
import datetime

# Load data
data = pd.read_csv(input("Enter the path to the CSV file: "), sep=",")

print(f"\nData loaded successfully!")
print(f"Shape: {data.shape[0]} rows, {data.shape[1]} columns\n")

report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Calculate quality metrics for the report
total_cells = len(data) * len(data.columns)
missing_cells = data.isnull().sum().sum()
completeness_score = ((total_cells - missing_cells) / total_cells) * 100

uniqueness_issues = sum([data.duplicated(subset=[col]).sum() for col in data.columns])
uniqueness_score = max(0, 100 - (uniqueness_issues / len(data) * 10))

overall_score = (completeness_score + uniqueness_score) / 2

# Outlier detection for the report
numeric_cols = data.select_dtypes(include=[np.number]).columns
outlier_summary = []

for col in numeric_cols:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
    
    if len(outliers) > 0:
        outlier_summary.append({
            'Column': col,
            'Outlier_Count': len(outliers),
            'Outlier_Percent': f"{(len(outliers)/len(data)*100):.2f}%",
            'Lower_Bound': f"{lower_bound:.2f}",
            'Upper_Bound': f"{upper_bound:.2f}"
        })

# Missing values report
missing_values = data.isnull().sum()
missing_percent = (missing_values / len(data)) * 100

missing_report = pd.DataFrame({
    'Column': missing_values.index,
    'Missing_Count': missing_values.values,
    'Missing_Percent': missing_percent.values
})

missing_report = missing_report[missing_report['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

# Duplicate check
duplicate_count = data.duplicated().sum()

# Print console summary
print("="*60)
print("DATA QUALITY SUMMARY")
print("="*60)
print(f"Overall Quality Score: {overall_score:.2f}%")
print(f"Completeness Score: {completeness_score:.2f}%")
print(f"Uniqueness Score: {uniqueness_score:.2f}%")
print(f"Duplicate Rows: {duplicate_count}")
print(f"Missing Values: {missing_cells}")
print(f"Outliers Detected: {len(outlier_summary)} columns")
print("="*60)

# Load HTML template
with open('report_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace placeholders with actual data
html_content = template.replace('{{report_date}}', report_date)
html_content = html_content.replace('{{total_rows}}', f"{len(data):,}")
html_content = html_content.replace('{{total_columns}}', str(len(data.columns)))
html_content = html_content.replace('{{duplicate_count}}', f"{duplicate_count:,}")
html_content = html_content.replace('{{missing_cells}}', f"{missing_cells:,}")
html_content = html_content.replace('{{overall_score}}', f"{overall_score:.1f}")
html_content = html_content.replace('{{completeness_score}}', f"{completeness_score:.2f}")
html_content = html_content.replace('{{uniqueness_score}}', f"{uniqueness_score:.2f}")
html_content = html_content.replace('{{score_class}}', 'excellent' if overall_score >= 90 else 'good' if overall_score >= 70 else 'poor')
html_content = html_content.replace('{{missing_report_html}}', missing_report.to_html(index=False) if len(missing_report) > 0 else '<p class="pass">No missing values found</p>')
html_content = html_content.replace('{{outlier_html}}', pd.DataFrame(outlier_summary).to_html(index=False) if outlier_summary else '<p class="pass">No outliers detected</p>')
html_content = html_content.replace('{{column_details_html}}', data.dtypes.to_frame('Data_Type').to_html())

# Save report
with open('data_quality_report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\nHTML report saved as 'data_quality_report.html'")
print("Open this file in your browser to view the detailed report.")
