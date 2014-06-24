DropboxAPI: dropbox_uploadFiles.py
==========
Скрипт для бекапа файлов/проектов в ваш аккаунт DropBox. 
Возможности: 
  1. исключать из бекапа опредленные директории (cache, fraemwork ...)
  2. исключать из бекапа опредленные файлы (db.log, config.py)
  3. исключать из бекапа опредленные расширения файлов (.cfg, .log, .backup)
  
Установка
==========
  1. Для начала вам нужно установить DropBoX CORE API: https://www.dropbox.com/developers/core/sdks/python
  2. Далее вам нужно создать новое приложение https://www.dropbox.com/developers/apps
  3. Создать  access token
  4. В скрипт dropbox_uploadFiles.py записать "App key" в "APP_KEY", "App secret" в "APP_SECRET", "access token" в "ACCESS_TOKEN"
  5. Добавить права на выполнение скрипта: chmod +x ./dropbox_uploadFiles.py
  
Использование
==========
Пример:
./dropbox_uploadFiles.py -s /opt/www/vhosts/my_website -t /remote_folder -i1 "temp|assets|cache|framework|log" -i2 config.py -i3 ".bin|.log"

  -s /opt/www/vhosts/my_website - директория нашего проекта, которого надо забекапить [ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР]
  
  -t /remote_folder - папка в DropBOX куда будет скопирован наш проект (если папки нету, то скрипт ее создаст) [ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР]
  
  -i1 "temp|assets|cache|framework|log" - директории, которые не нужно копировать (будут проигнорированы)
  
  -i2 "config.py" - файлы, которые не нужно копировать (будут проигнорированы)
  
  -i3 ".bin|.log" - расширения файлов, которые не нужно копировать (такие файлы будут проигнорированы)

