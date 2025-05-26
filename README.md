# Voice Cloning API

## Tổng quan

Dự án đã được tái cấu trúc thành một kiến trúc modular rõ ràng và các API đã được cập nhật để trả về audio buffer thay vì lưu file.

## Cấu trúc thư mục mới

```
app/
├── __init__.py
├── main.py                 # Entry point chính
├── config/
│   ├── __init__.py
│   └── settings.py         # Cấu hình tập trung
├── models/
│   ├── __init__.py
│   ├── requests.py         # Pydantic request models
│   └── responses.py        # Pydantic response models
├── services/
│   ├── __init__.py
│   ├── voice_service.py    # Logic xử lý voice cloning
│   └── audio_service.py    # Logic xử lý audio
├── utils/
│   ├── __init__.py
│   ├── file_utils.py       # Utilities cho file
│   └── audio_utils.py      # Utilities cho audio
└── api/
    ├── __init__.py
    ├── health.py           # Health check endpoints
    ├── voice_extraction.py # Voice extraction endpoints
    ├── voice_cloning.py    # Voice cloning endpoints
    └── file_management.py  # File management endpoints
```

## Thay đổi chính

### 1. Cấu trúc modular
- **Config**: Tất cả cấu hình được tập trung trong `app/config/settings.py`
- **Models**: Pydantic models được tách riêng cho requests và responses
- **Services**: Logic nghiệp vụ được tách thành các service classes
- **Utils**: Các utility functions được nhóm theo chức năng
- **API**: Endpoints được tách thành các modules riêng biệt

### 2. API trả về audio buffer
- **Mặc định**: Tất cả API audio giờ trả về base64 encoded audio buffer
- **Tùy chọn**: Có thể chọn trả về file path thông qua parameter `return_buffer=False`
- **Tự động dọn dẹp**: Files tạm được tự động xóa khi trả về buffer

### 3. Cải thiện hiệu suất
- **Thread pool**: Xử lý CPU-intensive tasks trong thread pool
- **Async/await**: Sử dụng async programming cho I/O operations
- **Memory efficient**: Giảm thiểu việc lưu trữ files không cần thiết

## API Endpoints

### Health Check
- `GET /health` - Kiểm tra trạng thái API

### Voice Extraction
- `POST /extract_voice` - Trích xuất voice embedding từ audio file
  - Parameter: `return_buffer=true` (mặc định) để trả về embedding buffer

### Voice Cloning
- `POST /clone_voice` - Clone voice với embedding có sẵn
- `POST /clone_voice_with_file` - Clone voice với file audio reference
  - Parameter: `return_buffer=true` (mặc định) để trả về audio buffer
- `GET /list_speakers` - Liệt kê speakers có sẵn

### File Management
- `GET /download/{filename}` - Download file (cho backward compatibility)
- `DELETE /cleanup/{filename}` - Xóa file cụ thể
- `GET /files` - Liệt kê files có sẵn
- `POST /cleanup_old_files` - Dọn dẹp files cũ

## Cách chạy

### 1. Chạy với backward compatibility
```bash
python main.py
```

### 2. Chạy trực tiếp app mới
```bash
python app/main.py
```

### 3. Chạy với uvicorn
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Ví dụ sử dụng API mới

### Extract voice embedding (trả về buffer)
```python
import requests
import base64

# Upload audio file và nhận embedding buffer
with open("voice_sample.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8000/extract_voice",
        files={"audio_file": f},
        params={"return_buffer": True}
    )

result = response.json()
embedding_buffer = result["embedding_buffer"]  # Base64 encoded embedding
```

### Clone voice với file (trả về audio buffer)
```python
import requests
import base64

# Upload reference audio và nhận cloned audio buffer
with open("reference_voice.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8000/clone_voice_with_file",
        files={"reference_audio": f},
        data={
            "text": "Xin chào, đây là giọng nói được nhân bản",
            "language": "VI",
            "speaker": "default",
            "speed": 0.9,
            "return_buffer": True
        }
    )

result = response.json()
audio_buffer = result["audio_buffer"]  # Base64 encoded audio

# Decode và lưu audio
audio_data = base64.b64decode(audio_buffer)
with open("cloned_voice.wav", "wb") as f:
    f.write(audio_data)
```

## Lợi ích của cấu trúc mới

1. **Maintainability**: Code được tổ chức rõ ràng, dễ bảo trì
2. **Scalability**: Dễ dàng thêm features mới
3. **Performance**: Giảm I/O operations, tự động dọn dẹp
4. **Flexibility**: Có thể chọn trả về buffer hoặc file
5. **Testing**: Dễ dàng test từng component riêng biệt

## Migration từ API cũ

- API cũ vẫn hoạt động thông qua `main.py`
- Để sử dụng features mới, chuyển sang endpoints mới với `return_buffer=True`
- Cập nhật client code để xử lý base64 audio buffers thay vì file paths
