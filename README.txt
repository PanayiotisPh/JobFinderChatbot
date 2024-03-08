commands
    docker:
        command: docker-compose up -d
    front-end:
        npm start dev
    rasa-chatbot:
        rasa run -m models\20240308-030246-champagne-lagoon.tar.gz --enable-api --cors "*" --debug

        rasa run actions
    
