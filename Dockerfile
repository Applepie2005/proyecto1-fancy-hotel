FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fancyhotel ./fancyhotel

WORKDIR /app/fancyhotel
ENV FANCYHOTEL_HOST=0.0.0.0
ENV FANCYHOTEL_PORT=5001
ENV FANCYHOTEL_DEBUG=0
ENV FANCYHOTEL_DB_HOST=mysql
ENV FANCYHOTEL_DB_PASSWORD=password

EXPOSE 5001
CMD ["python", "serve.py"]
