commands
    docker:
        command: docker-compose up -d
    front-end:
        npm start dev
    rasa-chatbot:
        rasa run -m models\20240209-010948-forgiving-flannel.tar.gz --enable-api --cors "*" --debug

        rasa run actions
    
