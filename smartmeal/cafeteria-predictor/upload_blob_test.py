from azure.storage.blob import BlobServiceClient

# Azurite용 연결 문자열 (local.settings.json과 동일하게 설정해야 함)
connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFeqCnb+...==;"  # 기본 Azurite 키
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

# 컨테이너 이름
container_name = "cafeteria"

# 업로드할 파일 이름
local_file_path = "trigger.csv"
blob_name = "trigger.csv"

# Blob 업로드
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# 컨테이너가 없으면 생성
try:
    container_client.create_container()
except Exception:
    pass  # 이미 존재하면 무시

# 업로드 실행
with open(local_file_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data, overwrite=True)

print(f"✅ 업로드 완료: {blob_name}")