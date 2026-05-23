#!/usr/bin/env python3
import json
import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
ENV_FILE = APP_DIR / ".env"
TOKEN_ENV_VAR = "DISCORD_BOT_TOKEN"


def load_env_file():
	"""Load key=value pairs from .env without overriding real environment vars."""
	if not ENV_FILE.exists():
		return

	with ENV_FILE.open("r", encoding="utf-8") as env_file:
		for line in env_file:
			line = line.strip()
			if not line or line.startswith("#") or "=" not in line:
				continue

			key, value = line.split("=", 1)
			key = key.strip()
			value = value.strip().strip('"').strip("'")

			if key and key not in os.environ:
				os.environ[key] = value


load_env_file()
CONFIG_FILE = os.getenv("CONFIG_FILE", str(APP_DIR / "config.json"))


def load_config():
	"""Load non-secret app settings from JSON if the file exists."""
	if not os.path.exists(CONFIG_FILE):
		return {}

	with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
		return json.load(config_file)


def get_bot_token():
	"""Read the Discord bot token from the environment."""
	token = os.getenv(TOKEN_ENV_VAR)
	if token:
		return token

	raise RuntimeError(
		f"Missing Discord bot token. Set the {TOKEN_ENV_VAR} environment variable."
	)
