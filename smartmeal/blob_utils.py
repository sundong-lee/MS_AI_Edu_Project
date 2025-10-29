from azure.storage.blob import BlobServiceClient
from config import AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_CONTAINER_NAME

# Blob 서비스 클라이언트 생성
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)

def upload_blob(file_bytes, blob_name):
    """
    파일 바이트를 Blob Storage에 업로드
    """
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file_bytes, overwrite=True)
    print(f"✅ 업로드 완료: {blob_name}")

def download_blob(blob_name):
    """
    Blob Storage에서 파일 다운로드 → 바이트 반환
    """
    blob_client = container_client.get_blob_client(blob_name)
    stream = blob_client.download_blob()
    return stream.readall()

def list_blobs():
    """
    컨테이너 내 모든 blob 목록 반환
    """
    return [blob.name for blob in container_client.list_blobs()]