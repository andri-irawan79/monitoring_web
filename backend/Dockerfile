# Konteks build = akar repositori (lihat docker-compose.yml). Tata letak dipertahankan agar simulator menemukan
# Crop_recommendationV2.csv di /srv (BASE_DIR = dua tingkat di atas simulator/).
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ /srv/backend/
COPY Crop_recommendationV2.csv /srv/Crop_recommendationV2.csv
COPY riset/data_simulasi_365.csv /srv/riset/data_simulasi_365.csv
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
