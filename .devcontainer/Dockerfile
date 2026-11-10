# syntax=docker/dockerfile:1
# ServiceFind development container for GitHub Codespaces
# Provides: Flutter 3.47.8 (Dart SDK included), Chromium for Flutter Web,
#           Python venv with FastAPI + Uvicorn, Git.
# Everything is installed inside the container only; nothing is required on the
# host machine (Windows/macOS/Linux).

FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# ---------------------------------------------------------------------------
# 1. System dependencies
#    - curl/wget: download Flutter SDK
#    - git: version control
#    - unzip/xz-utils: extract Flutter tarball
#    - libglu1-mesa/fontconfig: Flutter dependencies on Linux
#    - chromium: browser for Flutter Web run/debug
# ---------------------------------------------------------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        wget \
        git \
        unzip \
        xz-utils \
        libglu1-mesa \
        fontconfig \
        chromium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# 2. Flutter SDK (stable) + Dart SDK (bundled with Flutter)
# ---------------------------------------------------------------------------
ENV FLUTTER_VERSION=3.47.8
ENV FLUTTER_HOME=/opt/flutter
ENV PATH="$FLUTTER_HOME/bin:$PATH"
# Chromium is the browser Flutter uses for `flutter run -d chrome` / Flutter Web.
ENV CHROME_EXECUTABLE=/usr/bin/chromium-browser

RUN set -ex \
    && curl -fsSL -o /tmp/flutter.tar.xz \
        "https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz" \
    && mkdir -p "$FLUTTER_HOME" \
    && tar -xf /tmp/flutter.tar.xz -C "$FLUTTER_HOME" --strip-components=1 \
    && rm -f /tmp/flutter.tar.xz \
    # Make the Flutter install writable by the codespace user so `flutter
    # precache` and future `flutter upgrade` can write to the SDK directory.
    && chown -R codespace:codespace "$FLUTTER_HOME"

# Expose Flutter to login shells as well as interactive shells
RUN echo 'export PATH=/opt/flutter/bin:$PATH' > /etc/profile.d/flutter.sh \
    && chmod +x /etc/profile.d/flutter.sh

# ---------------------------------------------------------------------------
# 3. Python virtual environment for the FastAPI backend
# ---------------------------------------------------------------------------
ENV VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"

RUN python3 -m venv "$VENV_PATH" \
    && "$VENV_PATH/bin/pip" install --upgrade pip setuptools wheel \
    && chown -R codespace:codespace "$VENV_PATH"

# Python dependencies (FastAPI + Uvicorn)
COPY requirements.txt /tmp/requirements.txt
RUN "$VENV_PATH/bin/pip" install --no-cache-dir -r /tmp/requirements.txt

# ---------------------------------------------------------------------------
# 4. Configure Flutter tooling as the codespace user (writes config to
#    /home/codespace/.flutter so it persists for the actual user)
# ---------------------------------------------------------------------------
USER codespace
WORKDIR /workspaces/ServiceFind

# Enable Flutter Web and download the web engine artifacts once at build time
RUN flutter config --enable-web \
    && flutter precache --web

# Mark the workspace and Flutter SDK as safe Git directories (avoids "dubious
# ownership" errors; Flutter itself is a git repository).
RUN git config --global --add safe.directory /workspaces/ServiceFind \
    && git config --global --add safe.directory /opt/flutter

# Add Flutter to the interactive shell PATH (bashrc)
RUN echo 'export PATH=/opt/flutter/bin:$PATH' >> ~/.bashrc

# ---------------------------------------------------------------------------
# 5. Container entry defaults
# ---------------------------------------------------------------------------
CMD ["sleep", "infinity"]
