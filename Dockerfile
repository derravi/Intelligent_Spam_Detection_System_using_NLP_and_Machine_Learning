#Docker File Code

FROM python:3.13.7

RUN mkdir -p intelligent_spam_detection_system

WORKDIR /intelligent_spam_detection_system

COPY . /intelligent_spam_detection_system

RUN pip install -r requirements.txt

ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn","Api:app","--host","0.0.0.0","--port","8000"]