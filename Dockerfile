# FROM --platform=linux/arm/v7 python:3.9.0b4-alpine3.12
FROM python:3.9.0b4-alpine3.12

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY main.py /bin/main.py
COPY bot.py /bin/bot.py
COPY bollsvenskan.py /bin/bollsvenskan.py
COPY config.yaml /bin

COPY root /var/spool/cron/crontabs/root

# Give execution rights on the cron job
RUN chmod +x /bin/main.py

CMD crond -l 2 -f
