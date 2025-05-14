FROM ollama/ollama:latest

# Python quraşdır
RUN apt-get update && apt-get install -y python3 python3-pip git

# İş qovluğunu təyin et
WORKDIR /app

# Tələb olunan paketləri kopyala və quraşdır
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Proqram fayllarını kopyala
COPY . .

# Llama3.2 modelini əvvəlcədən yüklə
RUN ollama pull llama3.2

# Port açıqla
EXPOSE 8501

# Ollama servisi və Streamlit-i işə sal
CMD sh -c "ollama serve & streamlit run app.py"
