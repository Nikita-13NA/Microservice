FROM python:3.9-slim

# Создаем директорию для нашего приложения
RUN mkdir -p /service/recommendations

# Копируем requirements.txt и устанавливаем зависимости
COPY recommendations/requirements.txt /service/recommendations/requirements.txt
WORKDIR /service/recommendations
RUN python -m pip install --no-cache-dir --disable-pip-version-check --progress-bar off -r requirements.txt

# Копируем protobufs и основной код в контейнер
COPY protobufs/ /service/protobufs/
COPY recommendations/ /service/recommendations/

# Генерируем Python-код из protobuf-файлов
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/recommendations.proto

# Открываем порт 50051
#EXPOSE 50053

# Устанавливаем точку входа
CMD ["python", "recommendations.py"]
