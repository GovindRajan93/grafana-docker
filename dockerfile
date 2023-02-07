#Install OS dependencies, Browsers & python modules
FROM registry.access.redhat.com/ubi8/python-36

COPY requirements.txt /tmp/

# Install dependencies
USER root
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-utils \
    xorg-x11-xauth dbus-glib -y -q

RUN mkdir /opt/app && chown -R default:root /opt/app
#RUN chown default:root /opt/app-root/geckodriver.log

# Install Firefox Driver
RUN curl -SL https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz > geckodriver.tar.gz
RUN tar -xvzf geckodriver.tar.gz -C /opt/app-root/bin/
RUN chmod +x /opt/app-root/bin/geckodriver
RUN rm -f geckodriver.tar.gz

#Install Firefox Browser
RUN curl -SL https://ftp.mozilla.org/pub/firefox/releases/102.6.0esr/linux-x86_64/en-US/firefox-102.6.0esr.tar.bz2 > Firefoxsetup.tar.bz2
RUN tar -xvf Firefoxsetup.tar.bz2 -C /opt/app-root/bin/
RUN chmod +x /opt/app-root/bin/firefox/firefox
RUN rm -f Firefoxsetup.tar.bz2

RUN chown default:root /opt/app-root/bin/geckodriver
RUN chown default:root /opt/app-root/bin/firefox/firefox

# Install Python dependencies for function
RUN pip install --upgrade pip -q
RUN pip install -r /tmp/requirements.txt -q

USER default

#Environment Variable
#ENV alert_value 1

#Copy the Script 
COPY grafana.py /opt/app-root/

#Entry-Point/CMD
ENTRYPOINT [ "python", "/opt/app-root/grafana.py" ]
