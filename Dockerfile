FROM --platform=linux/arm/v7 python:3.9.0b4-alpine3.12
# FROM python:3.9.0b4-alpine3.12

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install C/C++ build tools
RUN apk add g++

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY main_bot.py /bin/main_bot.py
COPY main_delete_reactions.py /bin/main_delete_reactions.py
COPY main_poll.py /bin/main_poll.py
COPY bollsvenskan.py /bin/bollsvenskan.py
COPY config.yaml /bin/config.yaml

COPY root /var/spool/cron/crontabs/root

# Give execution rights
RUN chmod +x /bin/main_bot.py
RUN chmod +x /bin/main_delete_reactions.py
RUN chmod +x /bin/main_poll.py

WORKDIR /bin

CMD ["python", "main_bot.py"];crond -l 2 -f
