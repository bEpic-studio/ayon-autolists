FROM python:3.11-alpine


# get uv and install to non-root location
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
RUN mv /root/.local/bin/uv /usr/local/bin/uv

# copy code
RUN mkdir /service
COPY pyproject.toml /service/pyproject.toml
COPY uv.lock /service/uv.lock
COPY processor /service/processor

WORKDIR /service

# create non-root user
RUN addgroup -S ayonuser && adduser -SH ayonuser -G ayonuser
RUN chown ayonuser:ayonuser -R /service
RUN chmod 777 -R /service

# run processor as ayonuser
USER ayonuser
ENV UV_CACHE_DIR=/service/.cache/uv
RUN uv sync --locked --no-dev
CMD ["uv", "run", "-m", "processor"]
