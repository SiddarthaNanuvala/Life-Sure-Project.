# LifeSure Insurance Data Analysis Project

## Overview
This repository contains a comprehensive data analysis and visualization project for LifeSure Insurance, focusing on customer risk assessment and insurance charge analysis. The project includes an interactive dashboard and detailed data analysis to help stakeholders make informed decisions.

## Features
- Interactive Dashboard built with Dash/Plotly
- Real-time data filtering and visualization
- Risk assessment model
- Comprehensive data analysis
- Business insights generation

## Project Structure
```
Life-Sure-Project/
├── dashboard.py              # Interactive dashboard implementation
├── LifeSure_Insurance_Analysis.ipynb  # Jupyter notebook with analysis
├── insurance.csv            # Dataset
└── requirements.txt         # Project dependencies
```

## Key Components

### 1. Interactive Dashboard
- Real-time data filtering capabilities
- Multiple visualization types
- Key metrics display
- Regional analysis
- Risk assessment tools

### 2. Visualizations
- Bar charts for regional analysis
- Scatter plots for age vs. charges
- Box plots for risk categories
- Correlation heatmaps
- Customer distribution pie charts

### 3. Key Metrics
- Total number of customers
- Average insurance charges
- Smoker ratio percentage
- High-risk customer percentage

### 4. Risk Assessment
- Classification of customers into risk categories:
  - High Risk: Smokers
  - Medium Risk: BMI ≥ 30
  - Low Risk: Others

## Technologies Used
- Python 3.x
- Dash/Plotly
- Pandas
- NumPy
- Matplotlib/Seaborn

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/SiddarthaNanuvala/Life-Sure-Project.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   python dashboard.py
   ```

4. Access the dashboard:
   - Open your web browser
   - Navigate to `http://127.0.0.1:8050`

## Features in Detail

### Interactive Filters
- Region selection dropdown
- Age range slider
- Smoker status checkboxes

### Visualizations
1. **Regional Analysis**
   - Average charges by region
   - Customer distribution across regions

2. **Risk Assessment**
   - Insurance charges by risk category
   - Distribution of risk categories

3. **Demographic Analysis**
   - Age vs. Insurance charges
   - Impact of smoking status

4. **Correlation Analysis**
   - Relationships between variables
   - Key factors affecting insurance charges

## Project Goals
- Analyze insurance charge patterns
- Identify risk factors
- Provide actionable insights
- Enable data-driven decision making

## Contributing
Feel free to submit issues and enhancement requests!


## Author
Siddartha Nanuvala

## Acknowledgments
- Dataset source: [Insurance Dataset](https://www.kaggle.com/mirichoi0218/insurance)
- ESILV - Data Science Program 
