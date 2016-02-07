FROM buildpack-deps:jessie-scm

# Install Ubuntu packages
RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    python-dev \
    python-sphinx\
    doxygen \
    graphviz \
    apt-utils

# Install Python packages
RUN pip install \
    docutils \
    sphinx_bootstrap_theme
    
CMD (cd doc && python sncn-xdoc/xdoc.py html)