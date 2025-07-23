#!/usr/bin/env python3
"""
Debug script untuk menguji endpoint bukti setor
"""
import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:5001"

def test_process_endpoint():
    """Test endpoint /api/bukti_setor/process"""
    print("=" * 60)
    print("🧪 TESTING BUKTI SETOR PROCESS ENDPOINT")
    print("=" * 60)
    
    # Cari file test di folder uploads
    uploads_folder = Path("uploads")
    test_files = []
    
    if uploads_folder.exists():
        pdf_files = list(uploads_folder.glob("*.pdf"))
        jpg_files = list(uploads_folder.glob("*.jpg"))
        png_files = list(uploads_folder.glob("*.png"))
        
        test_files.extend(pdf_files)
        test_files.extend(jpg_files)
        test_files.extend(png_files)
    
    if not test_files:
        print("❌ Tidak ada file test ditemukan di folder uploads/")
        print("💡 Silakan letakkan file PDF atau gambar di folder uploads/")
        return False
    
    # Test dengan file pertama yang ditemukan
    test_file = test_files[0]
    print(f"🔍 Menggunakan file test: {test_file}")
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': f}
            print(f"📤 Mengirim request ke {BASE_URL}/api/bukti_setor/process...")
            
            response = requests.post(
                f"{BASE_URL}/api/bukti_setor/process", 
                files=files,
                timeout=30
            )
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Response berhasil!")
                print("📋 STRUKTUR RESPONSE:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # Verify structure
                if isinstance(data, dict):
                    print(f"\n🔍 ANALISIS STRUKTUR:")
                    print(f"   - success: {data.get('success')}")
                    print(f"   - total_halaman: {data.get('total_halaman')}")
                    print(f"   - results: {type(data.get('results'))}")
                    print(f"   - results length: {len(data.get('results', []))}")
                    
                    if data.get('results'):
                        for i, result in enumerate(data['results']):
                            print(f"   - Result {i+1}: {result}")
                    else:
                        print("   ⚠️ Results array kosong!")
                        
                else:
                    print(f"⚠️ Response bukan dictionary: {type(data)}")
                    print(f"Raw response: {data}")
                    
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON: {e}")
                print(f"Raw response text: {response.text}")
                return False
        else:
            print(f"❌ Error response:")
            print(f"   Status: {response.status_code}")
            print(f"   Text: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Tidak dapat terhubung ke server!")
        print("💡 Pastikan backend sudah running di port 5001")
        return False
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def check_server_status():
    """Check apakah server aktif"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ Server aktif - Status: {response.status_code}")
        return True
    except:
        print(f"❌ Server tidak aktif di {BASE_URL}")
        return False

if __name__ == "__main__":
    print("🚀 Memulai debug bukti setor endpoint...")
    
    # Check server status
    if not check_server_status():
        print("💡 Jalankan backend dengan: python app.py")
        exit(1)
    
    # Test process endpoint
    success = test_process_endpoint()
    
    print("\n" + "=" * 60)
    print("📋 HASIL DEBUG:")
    print(f"Process Endpoint: {'✅ PASS' if success else '❌ FAIL'}")
    print("=" * 60)
    
    if not success:
        print("\n💡 LANGKAH SELANJUTNYA:")
        print("1. Periksa log backend di terminal")
        print("2. Pastikan file test ada di folder uploads/")
        print("3. Pastikan POPPLER_PATH dikonfigurasi dengan benar")
        print("4. Pastikan EasyOCR terinstall: pip install easyocr")
