FROM python:3.9-slim
RUN pip install --no-cache-dir flask
COPY ./static /home/myapp/static/
COPY ./templates /home/myapp/templates/
COPY sample_app.py /home/myapp/
EXPOSE 6789
CMD python3 /home/myapp/sample_app.py
