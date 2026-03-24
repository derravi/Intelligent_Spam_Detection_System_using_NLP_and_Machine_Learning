FROM pyton:3.13.7

RUN mkdir -p intelligent_spam_detection_system  

WORKDIR /intelligent_spam_detection_system

COPY . /intelligent_spam_detection_system

RUN pip install -r requirements.txt

