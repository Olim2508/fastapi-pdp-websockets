FROM python:3.10.4-alpine3.15

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Tashkent \
    LANG=C.UTF-8 \
    APP_HOME=/usr/src/web

WORKDIR $APP_HOME

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu

RUN apk update && \
    apk add --no-cache curl postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev netcat-openbsd build-base alembic && \
    pip install --upgrade pip setuptools poetry && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID"

COPY ["app/pyproject.toml", "app/poetry.lock", "$APP_HOME/"]

COPY ./app/requirements.txt $APP_HOME

# todo fix poetry installing deps
# RUN poetry install

RUN pip install -r requirements.txt

COPY --chown=$USER:$USER ./docker/dev/web/entrypoints /
COPY --chown=$USER:$USER ./app $APP_HOME

RUN chmod +x /*.sh && \
    mkdir -p $APP_HOME/static && \
    chown -R $USER:$USER $APP_HOME

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--reload"]

USER $USER
