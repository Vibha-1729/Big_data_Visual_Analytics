# 🇮🇳 India Census Data Explorer

**An Interactive Dashboard for Exploring India’s 2011 Census Data**  
_Project for CS661: Data Visualization, IIT Kanpur_  

---

## 🌍 Overview
India’s 2011 Census contains a treasure of demographic insights—literacy, employment, population, and more.  
But in raw form (massive CSV/Excel sheets), it is dense and inaccessible.  

This project transforms static census tables into a **dynamic, interactive visualization platform** built with **Plotly Dash**.  
It empowers users—policy makers, researchers, and students—to **explore, compare, and analyze** India’s socio-economic landscape.  

---

## ✨ Features

### 🗺 State-Level Analysis
- Interactive **choropleth maps** of Indian states.  
- Attribute-wise **rankings, pie charts, and box plots**.  
- **Correlation heatmaps** to reveal inter-relationships.  

### 📍 District Drilldown
- District-level choropleths with **Top 5 / Bottom 5 highlights**.  
- **Bubble & scatter plots** to visualize attribute-population dynamics.  
- Rich **summary tables** with performance indicators.  

### ⚖️ Comparison Mode
- **Side-by-side state comparisons** with radar charts and dual maps.  
- **Development pathway analysis**: current vs potential performance.  
- Automated **textual insights** like “Kerala outperforms the national average by 15% in literacy.”  

### 📊 Statistical Toolkit
- Box plots for distributions, quartiles, and outliers.  
- Correlation matrices across literacy, employment, and gender metrics.  
- Dynamic dashboards updated with every user interaction.  

---

## 🛠 Tech Stack
- **Framework:** Plotly Dash (Python)  
- **Visualization:** Plotly Express, Graph Objects  
- **Data Processing:** Pandas, NumPy, GeoPandas  
- **Mapping:** GeoJSON for boundaries (states/districts)  

---

## 🔄 Data Pipeline
1. **Extract** raw census data from CSV/Excel.  
2. **Transform** → normalize values, fix datatypes, unify labels.  
3. **Load** into cleaned datasets integrated with GeoJSON for spatial analysis.  

---

## ⚡ Challenges & Solutions
- **High-dimensional data** → Normalized to consistent metrics.  
- **GeoJSON mismatches** → Name-mapping scripts in preprocessing.  
- **Evolving geography** → Telangana & Ladakh handled with flags/greyed visuals.  
- **Performance issues** → Optimized callbacks and component interactivity.  
- **Visual clarity** → Designed responsive charts & structured insights.  

---

## 🚀 Quick Start

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/CS661.git
cd CS661
```

### 2️⃣ Install Dependencies
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### 3️⃣ Run App
```bash
python app.py
```  
Open **http://127.0.0.1:8050/** in your browser 🎉  

---

## 👥 Contributors
👨‍💻 Aditya Anand  
👨‍💻 Abdul Ahad  
👨‍💻 Tanish Bansal  
👨‍💻 Aurav Pratap Singh  
👨‍💻 Kartikey Tomar  
👩‍💻 Vibha Narayan  
👩‍💻 Ananya Pandey  
👩‍💻 Ruchika Raj  

---

## 📜 License
MIT License – see [LICENSE](LICENSE) for details.  

---

## 🌟 Acknowledgments
This project was developed as part of **CS661 (Data Visualization)** at **IIT Kanpur**, under the guidance of faculty mentors.  
It bridges **data science & storytelling**, turning raw census data into a meaningful narrative for India’s future.  
