FROM ubuntu:16.04

COPY . . 

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv \
    && python3.6 -m pip install pip --upgrade \
    && apt-get install --yes curl \
    && curl --silent --location https://deb.nodesource.com/setup_4.x | bash - \
    && apt-get install -y nodejs

#    && apt-get install -y git

#RUN git clone https://github.com/CriMenghini/daf-QuAR.git
RUN python3 -m pip install -r requirements.txt
RUN npm install -g mapshaper

#WORKDIR /daf-QuAR
EXPOSE 5000

ENTRYPOINT [ "python3", "./portale.py" ]

