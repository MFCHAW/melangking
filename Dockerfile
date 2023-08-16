from python:3.9.0
expose 8501
cmd mkdir -p /app
WORKDIR /app
copy requirements.txt ./requirements.txt
#pyodbc
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc unixodbc-dev
RUN python3 -m pip install -r requirements.txt
#run pip3 install -r requirements.txt
copy . .
ENTRYPOINT ["streamlit", "run"]
CMD ["1_📊_Home.py"]