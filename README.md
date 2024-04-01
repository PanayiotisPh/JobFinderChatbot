# Job Finder
## Requirements
```bash=
python 3.10.0
React.js 18.2.0
Docker
```
## Installation Guide
```bash=
pip install -r requirements.txt

cd docker
docker-compose up -d

cd front-end
npm install
```
## How to run
```bash=
1) Open docker and make sure Users and Docker containers are running
2) Go to mongodb-api and run the .py file with python
3) Go to scrapper and run python data_extractor_manager.py
4) Once finished go to rasa-chatbot and in 2 seperate terminals run
   rasa run actions
   rasa run -m models\20240402-012837-hot-bias.tar.gz --enable-api --cors "*"
5) Open front-end folder and run
   npm start dev
```
