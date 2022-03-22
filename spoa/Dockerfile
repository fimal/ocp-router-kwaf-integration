FROM python:3.10.0-alpine3.15

ARG USER_UID=65534
ARG USER_GID=$USER_UID
ARG DEBUG_TOOLS
# Install debug tools ~ 100MB (if DEBUG_TOOLS is set to true)
RUN if [ "$DEBUG_TOOLS" = "true" ] ; then apk add -U vim strace net-tools curl git netcat-openbsd ; fi
RUN apk add --no-cache apk-tools && apk add --no-cache shadow && apk upgrade --no-cache

#COPY requirements.txt 
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY agent.py .

RUN  chown -R $USER_UID:$USER_GID /app
CMD ["python3","agent.py","--enforcer_svc_host","waas-enforcer-service.kwaf.svc", "--enforcer_svc_port","80"]

REPLACE_WITH_LABELS