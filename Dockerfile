
FROM python:3.9.10


RUN pip install Flask gunicorn line_bot_sdk requests Flask-Session Flask-SQLAlchemy sqlalchemy pymysql pg8000 line-bot-sdk pytz backtesting yfinance scipy



COPY src/ /app
WORKDIR /app


ENV PORT 8080


CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
