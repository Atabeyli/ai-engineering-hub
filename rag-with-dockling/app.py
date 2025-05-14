import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Excel Söhbət Proqramı", layout="wide")

st.title("Excel ilə Söhbət Proqramı")
st.write("Excel faylınızı yükləyin və məlumatlar haqqında suallar verin!")

uploaded_file = st.file_uploader("Excel faylı seçin", type=["xlsx", "csv", "xls"])

if uploaded_file:
    # Faylı oxu
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"Fayl uğurla yükləndi: {uploaded_file.name}")
        
        # Əsas məlumatlar
        st.header("Excel Faylının Ümumi Məlumatları")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Sətirlərin sayı:** {df.shape[0]}")
            st.write(f"**Sütunların sayı:** {df.shape[1]}")
            
        with col2:
            st.write(f"**Sütunlar:** {', '.join(df.columns)}")
        
        # Faylın tərkibi
        with st.expander("Excel faylının məzmunu"):
            st.dataframe(df)
        
        # Sual-cavab hissəsi
        st.header("Excel Faylı Haqqında Suallar")
        
        question = st.text_input("Sualınızı yazın (məsələn: 'Hansı sütunlar var?', 'Cəmi neçə sətir var?', 'X sütununun ortalaması nədir?')")
        
        if question:
            st.subheader("Cavab:")
            
            # Sualları emal et
            question_lower = question.lower()
            
            if any(word in question_lower for word in ["sütun", "sütunlar", "column", "columns"]):
                st.write(f"Faylda bu sütunlar var: {', '.join(df.columns)}")
                
            elif any(word in question_lower for word in ["sətir", "sətr", "row", "rows", "neçə sətir"]):
                st.write(f"Faylda cəmi {df.shape[0]} sətir var.")
                
            elif any(word in question_lower for word in ["ortalama", "orta", "mean", "average"]):
                # Sütun adını tapmağa çalış
                col_names = []
                for col in df.columns:
                    if col.lower() in question_lower:
                        col_names.append(col)
                
                if col_names:
                    for col in col_names:
                        if pd.api.types.is_numeric_dtype(df[col]):
                            st.write(f"**{col}** sütununun ortalaması: {df[col].mean()}")
                        else:
                            st.write(f"**{col}** sütunu ədədi deyil, ona görə ortalama hesablana bilməz.")
                else:
                    st.write("Hansı sütunun ortalamasını hesablamaq lazımdır? Aşağıdan bir sütun seçin:")
                    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                    if numeric_cols:
                        selected_col = st.selectbox("Sütun seçin:", numeric_cols)
                        st.write(f"**{selected_col}** sütununun ortalaması: {df[selected_col].mean()}")
                    else:
                        st.write("Faylda ədədi sütunlar yoxdur.")
            
            elif any(word in question_lower for word in ["maksimum", "max", "ən böyük", "ən çox"]):
                # Sütun adını tapmağa çalış
                col_names = []
                for col in df.columns:
                    if col.lower() in question_lower:
                        col_names.append(col)
                
                if col_names:
                    for col in col_names:
                        if pd.api.types.is_numeric_dtype(df[col]):
                            st.write(f"**{col}** sütununun maksimum dəyəri: {df[col].max()}")
                        else:
                            st.write(f"**{col}** sütunu ədədi deyil.")
                else:
                    st.write("Hansı sütunun maksimum dəyərini bilmək istəyirsiniz? Aşağıdan bir sütun seçin:")
                    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                    if numeric_cols:
                        selected_col = st.selectbox("Sütun seçin:", numeric_cols)
                        st.write(f"**{selected_col}** sütununun maksimum dəyəri: {df[selected_col].max()}")
                    else:
                        st.write("Faylda ədədi sütunlar yoxdur.")
            
            elif any(word in question_lower for word in ["minimum", "min", "ən kiçik", "ən az"]):
                # Sütun adını tapmağa çalış
                col_names = []
                for col in df.columns:
                    if col.lower() in question_lower:
                        col_names.append(col)
                
                if col_names:
                    for col in col_names:
                        if pd.api.types.is_numeric_dtype(df[col]):
                            st.write(f"**{col}** sütununun minimum dəyəri: {df[col].min()}")
                        else:
                            st.write(f"**{col}** sütunu ədədi deyil.")
                else:
                    st.write("Hansı sütunun minimum dəyərini bilmək istəyirsiniz? Aşağıdan bir sütun seçin:")
                    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                    if numeric_cols:
                        selected_col = st.selectbox("Sütun seçin:", numeric_cols)
                        st.write(f"**{selected_col}** sütununun minimum dəyəri: {df[selected_col].min()}")
                    else:
                        st.write("Faylda ədədi sütunlar yoxdur.")
                    
            elif any(word in question_lower for word in ["qrafik", "çəkmək", "göstər", "chart", "plot", "visualize"]):
                st.write("Qrafik çəkmək üçün bir sütun seçin:")
                numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                if numeric_cols:
                    selected_col = st.selectbox("Sütun seçin:", numeric_cols)
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.hist(df[selected_col], bins=20)
                    ax.set_title(f"{selected_col} sütununun histoqramı")
                    ax.set_xlabel(selected_col)
                    ax.set_ylabel("Tezlik")
                    st.pyplot(fig)
                else:
                    st.write("Faylda ədədi sütunlar yoxdur.")
                
            else:
                st.write("Təəssüf ki, bu sualı başa düşə bilmədim. Zəhmət olmasa, sütunlar, sətirlər, ortalama, maksimum, minimum və ya qrafik haqqında sual verin.")
        
        # Statistika və Analiz Hissəsi
        st.header("Statistik Analiz")
        
        # Ədədi sütunlar üçün statistikalar
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            with st.expander("Ədədi sütunlar üçün statistika"):
                st.dataframe(df.describe())
        
        # Qrafik analiz
        st.subheader("Qrafik Analiz")
        
        if numeric_cols:
            # Qrafik tipi seçimi
            chart_type = st.selectbox("Qrafik tipi seçin:", ["Histoqram", "Xətti qrafik", "Sütunlu qrafik", "Nöqtəli qrafik"])
            
            # Sütun seçimi
            selected_col = st.selectbox("Sütun seçin:", numeric_cols, key="chart_select")
            
            if chart_type == "Histoqram":
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.hist(df[selected_col], bins=20)
                ax.set_title(f"{selected_col} sütununun histoqramı")
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Tezlik")
                st.pyplot(fig)
                
            elif chart_type == "Xətti qrafik":
                st.line_chart(df[selected_col])
                
            elif chart_type == "Sütunlu qrafik":
                st.bar_chart(df[selected_col])
                
            elif chart_type == "Nöqtəli qrafik":
                if len(numeric_cols) > 1:
                    second_col = st.selectbox("İkinci sütun seçin:", [col for col in numeric_cols if col != selected_col])
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.scatter(df[selected_col], df[second_col])
                    ax.set_title(f"{selected_col} və {second_col} arasında əlaqə")
                    ax.set_xlabel(selected_col)
                    ax.set_ylabel(second_col)
                    st.pyplot(fig)
                else:
                    st.write("Nöqtəli qrafik üçün ən azı iki ədədi sütun lazımdır.")
        else:
            st.info("Faylda ədədi sütunlar olmadığı üçün qrafik analiz mümkün deyil.")
    
    except Exception as e:
        st.error(f"Fayl oxunarkən xəta baş verdi: {str(e)}")
else:
    st.info("Zəhmət olmasa, Excel faylı yükləyin.")
    
    # Nümunə fayl yaratmaq üçün düymə
    if st.button("Nümunə Excel faylı yarat"):
        # Nümunə məlumatlar yarat
        data = {
            'Ad': ['Əli', 'Anar', 'Aynur', 'Elşən', 'Fidan', 'Gülnar', 'İlham', 'Kənan', 'Leyla', 'Məryəm'],
            'Yaş': [25, 32, 28, 41, 23, 35, 29, 44, 26, 31],
            'Maaş': [1200, 2500, 1800, 3200, 1100, 2800, 1900, 3500, 1300, 2200],
            'Şöbə': ['IT', 'Satış', 'Marketing', 'İdarəetmə', 'IT', 'Satış', 'Marketing', 'İdarəetmə', 'IT', 'Satış'],
            'İş təcrübəsi (il)': [2, 7, 4, 12, 1, 9, 5, 15, 3, 6]
        }
        
        # Məlumatları DataFrame-ə çevir
        sample_df = pd.DataFrame(data)
        
        # Excel faylı kimi yüklə
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            sample_df.to_excel(writer, index=False, sheet_name='Işçilər')
        
        # İstifadəçiyə yüklə
        st.download_button(
            label="Nümunə Excel faylını yüklə",
            data=buffer.getvalue(),
            file_name="numune_isci_melumatlari.xlsx",
            mime="application/vnd.ms-excel"
        )
