addr="0.0.0.0:8000"

# Pipelines
echo "Pipelines:"
curl -s http://${addr}/api/v1/pipeline/info | jq

# Adding new topic
echo "Adding new sport topic"
curl -s -X POST "http://${addr}/api/v1/topic" \
    -H "Content-Type: application/json" \
    --data @- <<'JSON' | jq
{
  "name": "sport",
  "description": "Sports related emails including games, training, scores, and team updates"
}
JSON

# Add new emails
echo "Adding labeled email (topic=sport)"
curl -s -X POST "http://${addr}/api/v1/emails" \
  -H "Content-Type: application/json" \
  --data @- <<'JSON' | jq
{
  "subject": "Match day lineup confirmed",
  "body": "The team lineup is finalized and training starts at 6pm",
  "topic": "sport"
}
JSON

echo "Adding weekend email"
curl -s -X POST "http://${addr}/api/v1/emails" \
  -H "Content-Type: application/json" \
  --data @- <<'JSON' | jq
{
  "subject": "Weekend plan",
  "body": "Let's decide where to go this weekend",
  "topic": "personal"
}
JSON

echo "Adding unlabled email"
curl -s -X POST "http://${addr}/api/v1/emails" \
  -H "Content-Type: application/json" \
  --data @- <<'JSON' | jq
{
  "subject": "Traveling to Costa Rica",
  "body": "Hey there! I am in a beautiful island just traveling. Guess how I got here.",
}
JSON

echo "Adding unlabled email"
curl -s -X POST "http://${addr}/api/v1/emails" \
  -H "Content-Type: application/json" \
  --data @- <<'JSON' | jq
{
  "subject": "State Fair",
  "body": "I almost forgot to tell you. We should meet up before the state fair.",
}
JSON

# Classify with new topic
echo "Classify new sport email"
curl -s -X POST "http://${addr}/api/v1/emails/classify" \
  -H "Content-Type: application/json" \
  --data @- <<'JSON' | jq
{
  "subject": "Training session moved to 7pm",
  "body": "The football match lineup is ready and team practice starts earlier today",
  "strategy": "topic"
}
JSON

# Classify with nearest-email similarity strategy
echo "Classify weekend-like email with nearest similarity strategy"
curl -s -X POST "http://${addr}/api/v1/emails/classify" \
  -H "Content-Type: application/json" \
  --data @- <<'JSON' | jq
{
  "subject": "Weekend outing ideas",
  "body": "Should we pick a place to go this weekend and make a plan?",
  "strategy": "nearest"
}
JSON

