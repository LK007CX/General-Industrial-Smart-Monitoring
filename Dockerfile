FROM gism-dev:v1.5
WORKDIR /app
COPY . .
RUN locale-gen zh_CN.UTF-8 &&\
  DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
RUN locale-gen zh_CN.UTF-8
ENV LANG zh_CN.UTF-8 
ENV LANGUAGE zh_CN:zh 
ENV LC_ALL zh_CN.UTF-8

COPY font/msyh.ttc /usr/share/fonts/msyh.ttc
COPY font/msyhbd.ttc /usr/share/fonts/msyh.ttc
COPY font/msyhl.ttc /usr/share/fonts/msyh.ttc

CMD ["export", "LANG=en_US.UTF-8"]
CMD ["/usr/bin/python3", "main.py"]