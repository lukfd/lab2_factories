
class TopicAlreadyExistException(Exception):
    def __init__(self, topic_name: str):
        self.topic_name = topic_name
        super().__init__(f"Topic '{topic_name}' already exists")

