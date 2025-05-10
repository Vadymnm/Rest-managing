FROM python:3.12
LABEL authors="telco"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD database.py .
#COPY . '/'.
COPY .  .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
