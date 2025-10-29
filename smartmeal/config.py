import os

# Azure Storage
AZURE_STORAGE_CONNECTION_STRING = os.getenv("DefaultEndpointsProtocol=https;AccountName=prostorageaccountlsd;AccountKey=XWIWMxVOZT4niLPTCBEB/iliodpASnSgz3h6J2f0NfKO/Q9ccpB0KnIW8EIUGB8CVcACJu2NypiU+AStT01Xqg==;EndpointSuffix=core.windows.net")
AZURE_STORAGE_CONTAINER_NAME = "cafeteria"

# Azure OpenAI
AZURE_OPENAI_ENDPOINT = os.getenv("https://pro-lsd-openai.openai.azure.com/")
AZURE_OPENAI_KEY = os.getenv("FFGvGK5udRdN2ZOQuc1uHmBN4VXVklqXYDv9VCq70AST8ls6uQcSJQQJ99BJACYeBjFXJ3w3AAABACOGJCTa")
AZURE_OPENAI_MODEL = "gpt-4o"  # 또는 gpt-35-turbo
AZURE_OPENAI_API_VERSION = "2024-12-01-preview" 

# 기타 설정
PAST_DATA_FILENAME = "past_data.csv"
FUTURE_DATA_FILENAME = "future_data.csv"
WEATHER_DATA_FILENAME = "future_weather.csv"