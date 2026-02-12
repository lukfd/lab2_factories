addr="0.0.0.0:8000"

curl -X POST "http://${addr}/api/v1/emails/classify" \
    -H "Content-Type: application/json" \
    -d "{\"subject\": \"Meeting tomorrow at 2pm\", \"body\": \"Let's discuss the quarterly budget and project deadlines\"}"

# curl http://${addr}/api/v1/pipeline/info