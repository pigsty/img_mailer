#!/bin/sh
sudo docker run -d --name mailer_instance -p 80:80 -i -t pigsty/img_mailer
