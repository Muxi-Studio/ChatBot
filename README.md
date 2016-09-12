# 聊天机器人

启动mongodb
  ```
  cd /usr/local/
  ./mongodb/bin/mongod -port 27017 -dbpath ./mongodb/data --logpath ./mongodb/log/chatbot.log&
  ```

启动app
  ```
  uwsgi --ini app.ini&
  ```
