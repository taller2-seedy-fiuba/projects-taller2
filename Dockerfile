FROM python:3.7
ADD . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]