"""
Script tải file từ Google Drive sử dụng gdown
Phương pháp chuyên dụng cho Google Drive
Cần cài đặt: pip install gdown
"""

import shutil
import zipfile
from pathlib import Path


def get_project_root():
    """Lấy thư mục gốc của project"""
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    return project_root


def create_directories():
    """Tạo các thư mục cần thiết"""
    project_root = get_project_root()
    data_dir = project_root / "data"
    processed_dir = data_dir / "processed"

    # Tạo thư mục nếu chưa tồn tại
    data_dir.mkdir(exist_ok=True)
    processed_dir.mkdir(exist_ok=True)

    return processed_dir


def extract_zip_file(zip_path, extract_to):
    """
    Giải nén file zip

    Args:
        zip_path (Path): Đường dẫn file zip
        extract_to (Path): Thư mục đích

    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    try:
        print(f"🗂️  Đang giải nén file: {zip_path.name}")
        print(f"📂 Đích: {extract_to}")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Lấy danh sách file trong zip
            file_list = zip_ref.namelist()
            print(f"📋 File zip chứa {len(file_list)} files:")

            # Hiển thị một vài file đầu
            for i, filename in enumerate(file_list[:5]):
                print(f"   - {filename}")
            if len(file_list) > 5:
                print(f"   ... và {len(file_list) - 5} files khác")

            # Giải nén tất cả files
            zip_ref.extractall(extract_to)

        print("✅ Giải nén thành công!")
        return True

    except zipfile.BadZipFile:
        print("❌ File không phải là zip hợp lệ!")
        return False
    except Exception as error:
        print(f"❌ Lỗi khi giải nén: {error}")
        return False


def cleanup_zip_file(zip_path):
    """
    Xóa file zip sau khi giải nén

    Args:
        zip_path (Path): Đường dẫn file zip cần xóa
    """
    try:
        if zip_path.exists():
            zip_path.unlink()
            print(f"🗑️  Đã xóa file zip: {zip_path.name}")
        return True
    except Exception as error:
        print(f"⚠️  Không thể xóa file zip: {error}")
        return False


def download_from_gdrive():
    """
    Tải file từ Google Drive sử dụng gdown và xử lý hoàn chỉnh
    """
    try:
        import gdown

        file_id = "1hnZHIH0eJJj92Mc6SljAkFpHNpaKxj06"
        url = f"https://drive.google.com/uc?id={file_id}"

        # Tạo thư mục đích
        processed_dir = create_directories()

        # Tên file tải về (trong thư mục scripts)
        download_path = Path(__file__).parent / "downloaded_data.zip"

        print("📥 Đang tải file từ Google Drive...")
        print(f"🔗 URL: {url}")
        print(f"💾 Tải về: {download_path}")
        print()

        # Tải file với gdown
        result = gdown.download(url, str(download_path), quiet=False)

        if not result or not download_path.exists():
            print("❌ Không thể tải file từ Google Drive")
            return False

        # Kiểm tra kích thước file
        file_size = download_path.stat().st_size
        print(f"✅ Đã tải xong: {download_path.name}")
        print(f"📊 Kích thước: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        print()

        # Kiểm tra xem có phải file zip không
        if not download_path.suffix.lower() == ".zip":
            print("⚠️  File tải về không phải là zip, đổi tên...")
            new_path = download_path.with_suffix(".zip")
            download_path.rename(new_path)
            download_path = new_path

        # Giải nén file
        extract_success = extract_zip_file(download_path, processed_dir)

        if not extract_success:
            print("❌ Không thể giải nén file")
            return False

        print()

        # Hiển thị kết quả
        print("📋 Nội dung thư mục data/processed:")
        try:
            for item in processed_dir.iterdir():
                if item.is_file():
                    size = item.stat().st_size
                    print(f"   📄 {item.name} ({size:,} bytes)")
                elif item.is_dir():
                    file_count = len(list(item.iterdir()))
                    print(f"   📁 {item.name}/ ({file_count} items)")
        except Exception as e:
            print(f"⚠️  Không thể liệt kê files: {e}")

        print()

        # Xóa file zip gốc
        cleanup_success = cleanup_zip_file(download_path)

        if extract_success and cleanup_success:
            print("🎉 Hoàn thành tất cả các bước!")
            return True
        else:
            print("⚠️  Một số bước không thành công hoàn toàn")
            return False

    except ImportError:
        print("❌ Chưa cài gdown.")
        print("Cài đặt bằng lệnh: pip install gdown")
        return False
    except Exception as error:
        print(f"❌ Lỗi khi tải/xử lý file: {error}")
        return False


def install_gdown_guide():
    """
    Hướng dẫn cài đặt gdown
    """
    print("📚 HƯỚNG DẪN CÀI ĐẶT GDOWN:")
    print("-" * 40)
    print("1️⃣  Cài đặt từ pip:")
    print("   pip install gdown")
    print()
    print("2️⃣  Hoặc từ conda:")
    print("   conda install -c conda-forge gdown")
    print()
    print("3️⃣  Kiểm tra cài đặt:")
    print("   python -c \"import gdown; print('Gdown đã cài đặt!')\"")
    print()
    print("4️⃣  Sau khi cài đặt, chạy lại script này!")


def show_project_structure():
    """
    Hiển thị cấu trúc thư mục project sau khi hoàn thành
    """
    try:
        project_root = get_project_root()
        data_dir = project_root / "data"

        if not data_dir.exists():
            print("📁 Thư mục data chưa được tạo")
            return

        print("🏗️  Cấu trúc thư mục project:")
        print(f"📁 {project_root.name}/")
        print("   📁 data/")

        if (data_dir / "processed").exists():
            print("      📁 processed/")
            processed_dir = data_dir / "processed"

            # Hiển thị nội dung processed
            items = list(processed_dir.iterdir())
            for i, item in enumerate(items[:10]):  # Chỉ hiển thị 10 items đầu
                is_last = i == len(items) - 1 or i == 9
                prefix = "         └── " if is_last else "         ├── "

                if item.is_file():
                    size = item.stat().st_size / (1024 * 1024)  # MB
                    print(f"{prefix}📄 {item.name} ({size:.2f} MB)")
                else:
                    sub_count = len(list(item.iterdir())) if item.is_dir() else 0
                    print(f"{prefix}📁 {item.name}/ ({sub_count} items)")

            if len(items) > 10:
                print(f"         └── ... và {len(items) - 10} items khác")

    except Exception as error:
        print(f"⚠️  Không thể hiển thị cấu trúc: {error}")


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TẢI VÀ XỬ LÝ DỮ LIỆU TỪ GOOGLE DRIVE")
    print("=" * 60)
    print()

    # Kiểm tra xem gdown đã được cài chưa
    try:
        import gdown  # noqa: F401

        print("✅ Gdown đã sẵn sàng!")
        print()

        success = download_from_gdrive()

        print("=" * 60)
        if success:
            print("🎉 HOÀN THÀNH TẤT CẢ CÁC BƯỚC!")
            print()
            show_project_structure()
        else:
            print("❌ QUÁ TRÌNH THẤT BẠI!")
            print("💡 Kiểm tra lại kết nối mạng và Google Drive link")
        print("=" * 60)

    except ImportError:
        print("❌ Gdown chưa được cài đặt!")
        print()
        install_gdown_guide()
        print("=" * 60)
