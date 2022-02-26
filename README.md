# signHyper

docker run -dit \
-v /root/software/ql/config:/ql/config \
-v /root/software/ql/log:/ql/log \
-v /root/software/ql/db:/ql/db \
-v /root/software/ql/scripts:/ql/scripts \
-v /root/software/ql/jbot:/ql/jbot \
-v /root/software/ql/repo:/ql/repo \
-p 5700-5705:5700-5705 \
-e ENABLE_HANGUP=true \
-e ENABLE_WEB_PANEL=true \
--name qinglong \
--hostname qinglong \
--restart always \
whyour/qinglong:latest