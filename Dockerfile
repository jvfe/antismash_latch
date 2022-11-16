FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:6839-main

RUN apt-get update &&\
    apt-get install -y curl

# Get miniconda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Get Mamba
RUN conda install -y mamba -n base -c conda-forge

# Get AntiSMASH
RUN mamba create -y -n antismash -c bioconda -c conda-forge antismash
ENV ANTIS_ENV $CONDA_DIR/envs/antismash
ENV PATH=$ANTIS_ENV/bin:$PATH

# Set shell
SHELL ["conda", "run", "-n", "antismash", "/bin/bash", "-c"]

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
RUN $CONDA_DIR/bin/pip install --upgrade latch
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
