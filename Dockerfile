FROM python:3.12-bullseye

COPY sandbox_reqs.txt /sandbox_reqs.txt
RUN pip install -r /sandbox_reqs.txt