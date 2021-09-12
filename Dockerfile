FROM python:3.9.6-buster

RUN useradd -ms /bin/bash auth_user
WORKDIR /src

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY --chown=auth_user:auth_user ["./pyproject.toml", "./poetry.lock*", "wsgi.py", "/src/"]
EXPOSE 5000

RUN poetry install --no-root

COPY --chown=auth_user:auth_user ["./", "/src"]
USER auth_user

CMD gunicorn -b :5000 --access-logfile - --error-logfile - wsgi:"create_app()"
