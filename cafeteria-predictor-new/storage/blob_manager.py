from azure.storage.blob import BlobServiceClient
from io import BytesIO
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "cafeteria"

blob_service = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
container_client = blob_service.get_container_client(CONTAINER_NAME)

def upload_to_blob(blob_name, file_or_df):
    """
    DataFrame 또는 업로드된 파일을 Azure Blob에 저장
    """
    if isinstance(file_or_df, pd.DataFrame):
        buffer = BytesIO()
        file_or_df.to_csv(buffer, index=False, encoding="utf-8-sig")
        buffer.seek(0)
        data = buffer
    else:
        # Streamlit file_uploader 객체 처리
        content = file_or_df.read()
        try:
            decoded = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            decoded = content.decode("cp949")
        data = BytesIO(decoded.encode("utf-8-sig"))

    container_client.upload_blob(name=blob_name, data=data, overwrite=True)

def download_from_blob(blob_name):
    """
    Azure Blob에서 CSV 파일을 읽어 DataFrame으로 반환
    """
    blob_client = container_client.get_blob_client(blob_name)
    stream = blob_client.download_blob().readall()

    try:
        return pd.read_csv(BytesIO(stream), encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(BytesIO(stream), encoding="cp949")