# 🔄 Update: Bukti Setor Navigation System

## 📋 Overview

Sistem preview bukti setor telah dimodifikasi untuk menggunakan sistem navigasi **next/previous** seperti pada faktur, menggantikan sistem scroll yang sebelumnya digunakan.

## 🔧 Perubahan yang Dilakukan

### 1. **Modifikasi Response Structure**

**Sebelum:**
```json
{
  "message": "Data berhasil diekstrak.",
  "data": [
    {
      "kode_setor": "411211",
      "tanggal": "2024-01-15",
      "jumlah": "100000",
      "preview_filename": "bukti_hal_1_abc123.jpg"
    }
  ]
}
```

**Sesudah:**
```json
{
  "success": true,
  "results": [
    {
      "preview_image": "bukti_hal_1_abc123.jpg",
      "data": {
        "kode_setor": "411211",
        "tanggal": "2024-01-15",
        "jumlah": "100000",
        "halaman": 1
      },
      "halaman": 1
    }
  ],
  "total_halaman": 1
}
```

### 2. **Bulk Save Support**

Endpoint `/api/bukti_setor/save` sekarang mendukung:
- **Single record save** (format existing)
- **Bulk save** untuk multiple records sekaligus

```javascript
// Bulk save
const bulkData = [
  { kode_setor: "411211", tanggal: "2024-01-15", jumlah: "100000" },
  { kode_setor: "411212", tanggal: "2024-01-16", jumlah: "200000" }
];

fetch('/api/bukti_setor/save', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(bulkData)
});
```

### 3. **Konsistensi dengan Faktur**

Response structure sekarang konsisten dengan sistem faktur:
- ✅ `success` flag
- ✅ `results` array dengan metadata
- ✅ `total_halaman` untuk navigation
- ✅ `preview_image` path
- ✅ `halaman` number untuk tracking

## 🎯 Benefits

### 1. **Improved User Experience**
- Navigation next/previous seperti faktur
- Consistent interface across modules
- Easier file management untuk multiple pages

### 2. **Better Performance**
- Tidak perlu scroll panjang untuk banyak file
- Loading per-page basis
- Memory efficient

### 3. **Enhanced Functionality**
- Bulk save support
- Individual page handling
- Better error handling per page

## 🚀 Frontend Integration

### Sample Implementation (React/Vue/Vanilla JS)

```javascript
class BuktiSetorNavigator {
  constructor() {
    this.currentPage = 0;
    this.totalPages = 0;
    this.results = [];
  }

  async processFiles(files) {
    const formData = new FormData();
    formData.append('file', files[0]);
    
    const response = await fetch('/api/bukti_setor/process', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    
    if (data.success) {
      this.results = data.results;
      this.totalPages = data.total_halaman;
      this.currentPage = 0;
      this.renderCurrentPage();
    }
  }

  renderCurrentPage() {
    const current = this.results[this.currentPage];
    
    // Update preview image
    document.getElementById('preview').src = `/api/bukti_setor/uploads/${current.preview_image}`;
    
    // Update form fields
    document.getElementById('kode_setor').value = current.data.kode_setor;
    document.getElementById('tanggal').value = current.data.tanggal;
    document.getElementById('jumlah').value = current.data.jumlah;
    
    // Update navigation
    document.getElementById('page-info').textContent = `${this.currentPage + 1} / ${this.totalPages}`;
    document.getElementById('prev-btn').disabled = this.currentPage === 0;
    document.getElementById('next-btn').disabled = this.currentPage === this.totalPages - 1;
  }

  nextPage() {
    if (this.currentPage < this.totalPages - 1) {
      this.currentPage++;
      this.renderCurrentPage();
    }
  }

  prevPage() {
    if (this.currentPage > 0) {
      this.currentPage--;
      this.renderCurrentPage();
    }
  }

  async saveAll() {
    // Collect all data
    const allData = this.results.map(result => result.data);
    
    const response = await fetch('/api/bukti_setor/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(allData)
    });
    
    if (response.ok) {
      alert('Semua data berhasil disimpan!');
    }
  }

  async saveCurrent() {
    const currentData = this.results[this.currentPage].data;
    
    const response = await fetch('/api/bukti_setor/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentData)
    });
    
    if (response.ok) {
      alert('Data halaman ini berhasil disimpan!');
    }
  }
}
```

## 📝 Migration Guide

### Untuk Frontend Developers:

1. **Update API Response Handler**
   ```javascript
   // OLD
   const data = response.data.data; // array langsung
   
   // NEW  
   const results = response.data.results; // structured array
   const totalPages = response.data.total_halaman;
   ```

2. **Update Preview Image Path**
   ```javascript
   // OLD
   const imagePath = `/preview/${item.preview_filename}`;
   
   // NEW
   const imagePath = `/api/bukti_setor/uploads/${result.preview_image}`;
   ```

3. **Implement Navigation Controls**
   ```html
   <div class="navigation">
     <button id="prev-btn" onclick="navigator.prevPage()">Previous</button>
     <span id="page-info">1 / 1</span>
     <button id="next-btn" onclick="navigator.nextPage()">Next</button>
   </div>
   ```

## 🧪 Testing

Untuk menguji perubahan, Anda bisa:
- Menggunakan aplikasi frontend
- Menjalankan unit tests di folder `tests/`
- Test manual melalui API endpoint

## 🔍 Files Modified

1. `bukti_setor/utils/bukti_setor_processor.py` - Response structure
2. `bukti_setor/routes.py` - Endpoint behavior + bulk save

## ⚠️ Breaking Changes

- Response format `/api/bukti_setor/process` telah berubah
- Frontend perlu update untuk handle struktur baru
- Preview image path menggunakan endpoint bukti_setor

## 📞 Support

Jika ada issue dengan implementasi baru:
1. Cek console logs untuk error
2. Verify response structure dengan test script
3. Pastikan preview images ter-generate dengan benar

---

**🎉 Update berhasil! Sistem bukti setor sekarang konsisten dengan faktur dan mendukung navigation yang lebih baik.**
