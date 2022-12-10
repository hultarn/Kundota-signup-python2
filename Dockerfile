# FROM --platform=linux/arm/v7 python:3.9.0b4-alpine3.12
FROM python:3.9.0b4-alpine3.12

COPY main.py /bin/main.py
COPY bot.py /bin/bot.py
COPY bollsvenskan.py /bin/bollsvenskan.py
COPY config.yaml /bin/config.yaml

COPY root /var/spool/cron/crontabs/root

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Give execution rights on the cron job
RUN chmod +x /bin/main.py

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

CMD crond -l 2 -f
