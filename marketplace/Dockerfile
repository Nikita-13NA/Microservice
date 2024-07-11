# Используем базовый образ Python 3.9 slim
FROM python:3.9-slim

# Создаем директорию для нашего приложения
RUN mkdir -p /service/marketplace

# Копируем requirements.txt и устанавливаем зависимости
COPY marketplace/requirements.txt /service/marketplace/requirements.txt
WORKDIR /service/marketplace
RUN python -m pip install --no-cache-dir --disable-pip-version-check --progress-bar off -r requirements.txt

# Копируем protobufs и основной код в контейнер
COPY protobufs/ /service/protobufs/
COPY marketplace/ /service/marketplace/

# Генерируем Python-код из protobuf-файлов
RUN python -m grpc_tools.protoc -I /service/protobufs --python_out=/service/marketplace --grpc_python_out=/service/marketplace /service/protobufs/recommendations.proto

# Устанавливаем рабочую директорию в /service/marketplace
WORKDIR /service/marketplace

# Открываем порт (если необходимо)
# EXPOSE 5001

# Устанавливаем точку входа для запуска приложения
CMD ["python", "marketplace.py"]
