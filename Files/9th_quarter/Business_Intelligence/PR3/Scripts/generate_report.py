# generate_report.py
import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import matplotlib
matplotlib.use('Agg')  # modo sin GUI
import matplotlib.pyplot as plt
import numpy as np

# ===== Configuración =====
output_path = "LazyLearning_Report_GermanCredit.pdf"
doc = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=50, bottomMargin=50)

# Estilos
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    spaceAfter=30,
    alignment=TA_CENTER,
    textColor=colors.darkblue
)
heading1 = ParagraphStyle(
    'CustomH1',
    parent=styles['Heading1'],
    fontSize=18,
    spaceBefore=20,
    spaceAfter=10,
    textColor=colors.darkgreen
)
heading2 = ParagraphStyle(
    'CustomH2',
    parent=styles['Heading2'],
    fontSize=14,
    spaceBefore=14,
    spaceAfter=6,
    textColor=colors.black
)
normal = ParagraphStyle(
    'CustomNormal',
    parent=styles['BodyText'],
    fontSize=11,
    leading=14,
    spaceAfter=6,
    alignment=TA_JUSTIFY
)
code = ParagraphStyle(
    'CustomCode',
    parent=styles['Code'],
    fontSize=9,
    leading=12,
    spaceAfter=8
)

# ===== Datos reales (tus resultados) =====
ranking_data = [
    ["arboles", "BernoulliNB", "0.7127", "0.7127", "0.7548", "0.019 s"],
    ["red_neuronal", "NearestCentroid", "0.6389", "0.6389", "0.6732", "0.009 s"],
    ["ensamble", "NearestCentroid", "0.6270", "0.6270", "0.6583", "0.013 s"],
    ["reg_logistica", "NearestCentroid", "0.6103", "0.6103", "0.6479", "0.019 s"]
]

preproc_summary = [
    ["Flujo", "Características Clave"],
    ["reg_logistica", "• Winsorización suave\n• One-Hot (drop_first)\n• Estandarización\n• Transformaciones log"],
    ["arboles", "• Winsorización robusta (3×IQR)\n• Codificación ordinal & target encoding\n• Interacciones manuales (ej: high_risk_profile)\n• Eliminación de variables poco relevantes"],
    ["ensamble", "• Recodificación semántica\n• Features acumulativas (risk_factor_count)\n• Target encoding regularizado\n• Feature selection (varianza/corr >0.9)"],
    ["red_neuronal", "• Winsorización conservadora\n• Embeddings (var_idx)\n• Normalización Min-Max\n• Features polinómicas y cíclicas (age_sin/cos)"]
]

# ===== Gráfico: Ranking AUC =====
plt.figure(figsize=(6, 3))
flujos = [r[0] for r in ranking_data]
aucs = [float(r[2]) for r in ranking_data]
colors_list = ['#2E8B57' if r[0] == 'arboles' else '#696969' for r in ranking_data]

bars = plt.bar(flujos, aucs, color=colors_list, edgecolor='black', alpha=0.8)
plt.ylim(0.6, 0.75)
plt.ylabel('ROC AUC', fontsize=11)
plt.title('Ranking por ROC AUC por flujo de preprocesamiento', fontsize=12)
for bar, auc in zip(bars, aucs):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
             f'{auc:.4f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
chart_path = "temp_ranking_chart.png"
plt.savefig(chart_path, dpi=150, bbox_inches='tight')
plt.close()

# ===== Contenido =====
story = []

# Portada
story.append(Paragraph("📊 Informe de Lazy Learning", title_style))
story.append(Paragraph("<b>Selección Automática de Modelo para German Credit Data</b>", 
                      ParagraphStyle('SubTitle', parent=styles['Normal'], fontSize=16, alignment=TA_CENTER, spaceAfter=40)))
story.append(Paragraph("Fecha: 12 de noviembre de 2025", normal))
story.append(Paragraph("Dataset: German Credit Data (1000 instancias, 20 features)", normal))
story.append(Spacer(1, 24))

# 1. Introducción
story.append(Paragraph("1. Introducción", heading1))
story.append(Paragraph(
    "Este informe resume los hallazgos del benchmark automatizado de modelos de aprendizaje automático "
    "aplicado al conjunto de datos <i>German Credit</i>. El objetivo es identificar la combinación óptima "
    "de <b>preprocesamiento + modelo</b> que maximice la capacidad predictiva, priorizando ROC AUC, "
    "equilibrio entre clases y eficiencia computacional.", normal))

# 2. Técnicas de Preprocesamiento
story.append(Paragraph("2. Técnicas de Preprocesamiento Implementadas", heading1))
story.append(Paragraph(
    "Se diseñaron cuatro estrategias especializadas, adaptadas a distintas familias de modelos:", normal))

preproc_table = Table(preproc_summary, colWidths=[1.5*inch, 4.5*inch])
preproc_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 11),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('FONTSIZE', (0,1), (-1,-1), 10),
]))
story.append(preproc_table)
story.append(Spacer(1, 12))

# 3. Modelos Evaluados
story.append(Paragraph("3. Modelos Probados", heading1))
story.append(Paragraph(
    "Se usó <b>LazyClassifier</b> (<tt>lazypredict</tt>), que evaluó automáticamente +30 algoritmos "
    "por flujo (ej: LogisticRegression, RandomForest, XGBoost, SVM, Naive Bayes, KNN, etc.) "
    "usando hold-out 70/30 y métricas estandarizadas.", normal))

# 4. Resultados Destacados
story.append(Paragraph("4. Resultados Destacados", heading1))
story.append(Paragraph(
    "El ranking final por <b>ROC AUC</b> (métrica principal para problemas con desbalance) es:", normal))

# Tabla de ranking
ranking_table_data = [["Flujo", "Mejor Modelo", "ROC AUC", "Bal. Acc.", "F1 Score", "Tiempo"]]
ranking_table_data.extend(ranking_data)

ranking_table = Table(ranking_table_data, colWidths=[1.0*inch, 1.3*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.9*inch])
ranking_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 11),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('BACKGROUND', (0,1), (-1,1), colors.lightgreen),  # highlight best row
    ('FONTSIZE', (0,1), (-1,-1), 10),
]))
story.append(ranking_table)
story.append(Spacer(1, 10))

# Gráfico
if os.path.exists(chart_path):
    story.append(Image(chart_path, width=5*inch, height=2.5*inch))
    story.append(Spacer(1, 12))

# 5. Conclusión y Recomendación
story.append(Paragraph("5. Conclusión y Recomendación Final", heading1))
story.append(Paragraph(
    "<b>✅ Mejor combinación empíricamente validada:</b>", heading2))
story.append(Paragraph(
    "<font color='green'><b>→ Preprocesamiento: <tt>arboles</tt></b></font><br/>"
    "<font color='green'><b>→ Modelo: <tt>BernoulliNB</tt></b></font>", normal))

story.append(Paragraph(
    "<b>Justificación:</b>", heading2))
story.append(Paragraph(
    "• <b>ROC AUC máximo (0.7127)</b>: mejor discriminación entre clases.<br/>"
    "• <b>Alta eficiencia</b>: entrenamiento en 19 ms — ideal para producción.<br/>"
    "• <b>Robustez</b>: Balanced Accuracy = ROC AUC → sin sesgo por desbalance (70% good / 30% bad).<br/>"
    "• <b>Factibilidad técnica</b>: BernoulliNB requiere features binarias; el flujo <tt>arboles</tt> "
    "produjo exactamente ese tipo de representación (one-hot + ordinal + interacciones binarias).", normal))

story.append(Paragraph(
    "<b>Recomendación adicional:</b>", heading2))
story.append(Paragraph(
    "Entrenar <tt>XGBoost</tt> o <tt>HistGradientBoostingClassifier</tt> <b>sobre el dataset "
    "<tt>data_preprocesada_arboles.csv</tt></b>, pues es muy probable que superen 0.75 AUC con tuning ligero, "
    "aprovechando la calidad del preprocesamiento sin sacrificar interpretabilidad.", normal))

# Footer
story.append(PageBreak())
story.append(Spacer(1, 50))
story.append(Paragraph(
    "<i>Este informe fue generado automáticamente mediante Lazy Learning Benchmarking.<br/>"
    "Código fuente: pipeline de preprocesamiento + lazypredict.Supervised.LazyClassifier</i>", 
    ParagraphStyle('Footer', fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))

# ===== Generar PDF =====
try:
    doc.build(story)
    print(f"✅ PDF generado con éxito: {os.path.abspath(output_path)}")
    
    # Limpiar archivo temporal
    if os.path.exists(chart_path):
        os.remove(chart_path)
        
except Exception as e:
    print(f"❌ Error al generar el PDF: {e}")
    # Intentar sin gráfico si falla matplotlib
    if os.path.exists(chart_path):
        os.remove(chart_path)
    # Reintentar sin imagen
    story_no_img = [elem for elem in story if not isinstance(elem, Image)]
    SimpleDocTemplate("LazyLearning_Report_BACKUP.pdf", pagesize=A4).build(story_no_img)
    print("⚠️ PDF de respaldo generado sin gráfico.")