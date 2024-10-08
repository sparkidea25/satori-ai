# FROM python:3.9-slim
# WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # RUN git clone https://github.com/streamlit/streamlit-example.git .

# RUN pip3 install -r requirements.txt

# EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]


# FROM python:3.9.20-slim
# WORKDIR /app

# RUN pip install --no-binary=h5py h5py
# COPY requirements.txt requirements.txt
# COPY requirements.txt /app/
# RUN pip install --upgrade pip

# RUN pip3 install h5py
# RUN pip install --upgrade setuptools 
# RUN pip install -r requirements.txt
# RUN usr/local/bin/python -m pip install --upgrade pip
# RUN /Users/user/Documents/malaria-prediction/default_model/env/bin/python -m pip install --upgrade pip
# RUN pip install --upgrade pip

# RUN apt-get update && apt-get install -y libhdf5-dev

# RUN HDF5_DIR=/opt/homebrew/Cellar/hdf5/1.14.3_1/  pip install --no-binary=h5py h5py
# RUN  HDF5_VERSION=1.14.3_1 pip install --no-binary=h5py h5py
# RUN CC="mpicc" HDF5_MPI="ON" HDF5_DIR=/opt/homebrew/Cellar/hdf5/1.14.3_1/  pip install --no-binary=h5py h5py


# RUN pip install 
# --no-cache-dir -r requirements.txt
# RUN pip install
# COPY . /app/
# RUN pip install -r requirements.txt
# COPY . .
# EXPOSE 8080
# # CMD ["python3", "main.py"]
# CMD ["python", "main.py"]

FROM python:3.12 

RUN mkdir /usr/src/app

COPY main.py /usr/src/app

COPY requirements.txt /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]



