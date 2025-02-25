# Application Clone Twitter
Сервис микроблогов (аналог twitter)

<!--Разработка приложения-->
## Разработка приложения (Ubuntu 24.04.2 LTS)

1. Установка Docker:
   * удаляем старые версии docker
   ```console
       for pkg in docker.io docker-doc 
       docker-compose docker-compose-v2 
       podman-docker containerd runc; do sudo apt-get remove $pkg; 
       done
   ```
   * обновляем базу данных пакетов Ubuntu
   ```console
        sudo apt-get update
   ```
   * добавляем официальный ключ Docker от GPG
   ```console
        sudo apt-get install ca-certificates curl
        sudo install -m 0755 -d /etc/apt/keyrings
        sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
        sudo chmod a+r /etc/apt/keyrings/docker.asc
   ```
   * создаем новый репозиторий откуда будет скачиваться приложение Docker
   ```console
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
          $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
          sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
   * обновляем базу данных пакетов Ubuntu
   ```console
     sudo apt-get update
   ```
   * устанавливаем Docker
   ```console
     sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
   * убедиться что установленно все верно запустив проверочный образ hello-world
    ```console
     sudo docker run hello-world
   ```
   * создаем новую группу пользователей
   ```console
     sudo groupadd docker
   ```
   * добавим себя (текущего пользователя в эту группу) (вместо $USER имя текущего пользователя)
   ```console
     sudo usermod -aG docker $USER
   ```
2. Создание виртуального окружения
   * переходим в корневую папку
   ```console
     cd ./python_advanced_diploma
   ```
   * создаем виртуальное окружение
   ```console
     python3 -m venv .venv
   ```
    * активируем виртуальное окружение
   ```console
     source ./.venv/bin/activate
   ```
    *  устанавливаем необходимые пакеты
   ```console
     pip install -r ./server/requirements.txt
   ```
    *  проверяем список установленных пакетов
   ```console
     pip freeze
   ```
3. Удаление данных старой БД (по необходимости)
```console
   cd ./python_advanced_diploma
   sudo rm -r db/data
```
4. Удаление старой миграции БД (по необходимости)
```console
   cd ./python_advanced_diploma
   sudo rm ./server/migrations/versions/*.*
```
5. Удаление/очистка всех данных Docker-а (контейнеры, образы, тома, сети) (по необходимости)
```console
   cd ./python_advanced_diploma
   docker stop $(docker ps -qa) ;docker rm $(docker ps -qa); docker rmi -f $(docker images -qa); docker volume rm $(docker volume ls -q); docker network rm $(docker network ls -q)
```
6. Запуск контейнеров основной и тестовой БД через Docker Compose
```console
   cd ./python_advanced_diploma
   docker compose -f docker-compose-dev.yml up
```
7. Cоздание миграции инициализации структуры БД приложения
```console
   cd ./python_advanced_diploma/server
   alembic revision --autogenerate -m "init_db"
   alembic upgrade head
```
8. Запуск серверной части приложения
```console
   cd ./python_advanced_diploma/server/app
   uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```
9. Запуск клиентской части приложения
   * В файле конфигурации Nginx ```./python_advanced_diploma/client/nginx.conf``` временно поменять настройки
     (для продакшн версии нужно все настройки вернуть обратно)
     * ```server localhost:5000;``` заменить на ```server server:5000;```
     * ```listen 80;``` заменить на ```listen 8080```;
   * Запуск в Docker-контейнере
    ```console
       cd ./python_advanced_diploma/client
       docker build . -t client && docker run -ti --network="host" -p 8080:8080 client
    ```
10. Тестирование приложения
```console
   cd ./python_advanced_diploma/server/tests
   pytest -v -s
 ```
11. Автоформатирование кода
```console
   cd ./python_advanced_diploma/server
   black --line-length 79 --check --diff . || black --line-length 79 . && isort --check-only --diff --profile black . || isort --line-length 79 --profile black .
```
12. Статический анализ кода через Flake8 и MyPy
```console
   cd ./python_advanced_diploma/server
   flake8 . 
   mypy --explicit-package-bases .
```
