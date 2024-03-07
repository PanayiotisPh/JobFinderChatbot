commands
    docker:
        command: docker-compose up -d
    front-end:
        npm start dev
    rasa-chatbot:
        rasa run -m models\20240307-214934-hoary-chair.tar.gz --enable-api --cors "*" --debug

        rasa run actions
    
