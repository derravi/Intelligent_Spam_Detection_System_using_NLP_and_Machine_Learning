FROM python:3.11

WORKDIR /intelligent_spam_detection_system

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x run.sh

EXPOSE 8000
EXPOSE 8501

CMD ["./run.sh"]