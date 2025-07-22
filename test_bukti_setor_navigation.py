"""
Test script untuk memverifikasi perubahan sistem navigation bukti setor
"""
import requests
import json
from pathlib import Path

# URL base untuk testing (sesuaikan dengan server Anda)
BASE_URL = "http://localhost:5001"

def test_bukti_setor_navigation():
    """Test untuk memverifikasi format response bukti setor sekarang konsisten dengan faktur"""
    
    print("=" * 60)
    print("🧪 TESTING BUKTI SETOR NAVIGATION SYSTEM")
    print("=" * 60)
    
    # Test dengan file sample (gunakan file dari uploads jika ada)
    test_file_path = "test_bukti_setor.pdf"  # Ganti dengan path file test Anda
    
    # Cari file test alternatif di folder uploads
    uploads_folder = Path("uploads")
    if uploads_folder.exists():
        pdf_files = list(uploads_folder.glob("*.pdf"))
        jpg_files = list(uploads_folder.glob("*.jpg"))
        
        if pdf_files:
            test_file_path = str(pdf_files[0])
            print(f"🔍 Menggunakan file test: {test_file_path}")
        elif jpg_files:
            test_file_path = str(jpg_files[0])
            print(f"🔍 Menggunakan file test: {test_file_path}")
    
    if not Path(test_file_path).exists():
        print(f"❌ Test file tidak ditemukan: {test_file_path}")
        print("💡 Silakan siapkan file test bukti setor untuk testing")
        print("💡 Atau letakkan file PDF/JPG di folder uploads/")
        return False
    
    try:
        # Test process endpoint
        with open(test_file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/bukti_setor/process", files=files)
        
        print(f"📤 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response berhasil!")
            
            # Verify new structure
            required_fields = ['success', 'results', 'total_halaman']
            for field in required_fields:
                if field in data:
                    print(f"✅ Field '{field}' tersedia")
                else:
                    print(f"❌ Field '{field}' tidak ditemukan")
                    return False
            
            # Check results structure
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                required_result_fields = ['preview_image', 'data', 'halaman']
                
                for field in required_result_fields:
                    if field in result:
                        print(f"✅ Result field '{field}' tersedia")
                    else:
                        print(f"❌ Result field '{field}' tidak ditemukan")
                        return False
                
                # Check data structure
                data_obj = result.get('data', {})
                required_data_fields = ['kode_setor', 'tanggal', 'jumlah', 'halaman']
                
                for field in required_data_fields:
                    if field in data_obj:
                        print(f"✅ Data field '{field}' tersedia")
                    else:
                        print(f"❌ Data field '{field}' tidak ditemukan")
                
                print(f"📊 Total halaman: {data.get('total_halaman')}")
                print(f"📋 Total results: {len(data.get('results', []))}")
                
                # Pretty print structure
                print("\n📋 STRUKTUR RESPONSE:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
            return True
        else:
            print(f"❌ Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def test_bulk_save():
    """Test untuk memverifikasi bulk save functionality"""
    
    print("\n" + "=" * 60)
    print("🧪 TESTING BULK SAVE FUNCTIONALITY")
    print("=" * 60)
    
    # Sample data untuk testing bulk save
    sample_data = [
        {
            "kode_setor": "411211",
            "tanggal": "2024-01-15",
            "jumlah": "100000"
        },
        {
            "kode_setor": "411212",
            "tanggal": "2024-01-16", 
            "jumlah": "200000"
        }
    ]
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/bukti_setor/save",
            json=sample_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📤 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Bulk save berhasil!")
            print(f"📝 Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Memulai testing sistem navigation bukti setor...")
    
    # Test navigation system
    navigation_test = test_bukti_setor_navigation()
    
    # Test bulk save (uncomment jika ingin test save)
    # bulk_save_test = test_bulk_save()
    
    print("\n" + "=" * 60)
    print("📋 HASIL TESTING:")
    print(f"Navigation System: {'✅ PASS' if navigation_test else '❌ FAIL'}")
    # print(f"Bulk Save: {'✅ PASS' if bulk_save_test else '❌ FAIL'}")
    print("=" * 60)
