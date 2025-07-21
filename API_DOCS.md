# 🌐 API Documentation

Dokumentasi lengkap untuk REST API Proyek Pajak Backend.

## 📋 Base URL

```
http://localhost:5001
```

## 🔐 Authentication

Saat ini API tidak memerlukan authentication. Untuk production, pertimbangkan untuk menambahkan:
- API Key authentication
- JWT tokens
- OAuth 2.0

## 📊 Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    // response data
  },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "details": {
    // error details
  }
}
```

## 🧾 Invoice API Endpoints

### 1. Process Invoice File

Memproses file faktur pajak menggunakan OCR untuk ekstraksi data.

```http
POST /api/process
```

**Parameters:**
- `file` (multipart/form-data): File PDF atau gambar
- `jenis` (string): Jenis faktur ("masukan" atau "keluaran")

**Request Example:**
```bash
curl -X POST \
  http://localhost:5001/api/process \
  -F "file=@invoice.pdf" \
  -F "jenis=masukan"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "no_faktur": "010.000-24.00000001",
    "tanggal": "2024-01-15",
    "nama_lawan_transaksi": "PT. Contoh Indonesia",
    "npwp_lawan_transaksi": "01.234.567.8-901.000",
    "dpp": 100000,
    "ppn": 11000,
    "keterangan": "Pembelian barang dan jasa"
  }
}
```

**Error Responses:**
- `400`: File tidak valid atau jenis tidak dikenali
- `500`: Error dalam pemrosesan OCR

### 2. Save Invoice Data

Menyimpan data faktur ke database.

```http
POST /api/save
```

**Request Body:**
```json
{
  "jenis": "masukan",
  "no_faktur": "010.000-24.00000001",
  "tanggal": "2024-01-15",
  "nama_lawan_transaksi": "PT. Contoh Indonesia",
  "npwp_lawan_transaksi": "01.234.567.8-901.000",
  "dpp": 100000,
  "ppn": 11000,
  "keterangan": "Pembelian barang dan jasa"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "message": "Data berhasil disimpan"
  }
}
```

**Error Responses:**
- `400`: Data tidak valid atau tidak lengkap
- `409`: Nomor faktur sudah ada
- `500`: Error database

### 3. Get Invoice History

Mengambil riwayat faktur yang telah disimpan.

```http
GET /api/history
```

**Query Parameters:**
- `jenis` (optional): Filter berdasarkan jenis ("masukan" atau "keluaran")
- `bulan` (optional): Filter berdasarkan bulan
- `limit` (optional): Limit jumlah data (default: 100)
- `offset` (optional): Offset untuk pagination (default: 0)

**Request Example:**
```bash
curl "http://localhost:5001/api/history?jenis=masukan&bulan=Januari&limit=10"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "jenis": "masukan",
      "no_faktur": "010.000-24.00000001",
      "tanggal": "2024-01-15",
      "nama_lawan_transaksi": "PT. Contoh Indonesia",
      "npwp_lawan_transaksi": "01.234.567.8-901.000",
      "dpp": 100000,
      "ppn": 11000,
      "keterangan": "Pembelian barang dan jasa",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10
}
```

### 4. Export to Excel

Mengekspor data faktur ke format Excel.

```http
GET /api/export
```

**Query Parameters:**
- `jenis` (optional): Filter berdasarkan jenis
- `bulan` (optional): Filter berdasarkan bulan

**Response:**
Binary Excel file dengan header `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

**Request Example:**
```bash
curl -o faktur_export.xlsx "http://localhost:5001/api/export?jenis=masukan"
```

### 5. Delete Invoice

Menghapus data faktur berdasarkan ID.

```http
DELETE /api/delete/{jenis}/{id}
```

**Path Parameters:**
- `jenis`: Jenis faktur ("masukan" atau "keluaran")
- `id`: ID faktur yang akan dihapus

**Request Example:**
```bash
curl -X DELETE http://localhost:5001/api/delete/masukan/1
```

**Response:**
```json
{
  "success": true,
  "message": "Data berhasil dihapus"
}
```

**Error Responses:**
- `404`: Data tidak ditemukan
- `500`: Error database

## 📄 Bukti Setor API Endpoints

### 1. Process Bukti Setor

Memproses file bukti setor menggunakan OCR untuk ekstraksi data.

```http
POST /api/bukti_setor/process
```

**Parameters:**
- `file` (multipart/form-data): File PDF atau gambar bukti setor

**Request Example:**
```bash
curl -X POST \
  http://localhost:5001/api/bukti_setor/process \
  -F "file=@bukti_setor.pdf"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "tanggal": "2024-01-15",
    "kode_setor": "411211",
    "jumlah": 100000
  }
}
```

### 2. Save Bukti Setor

Menyimpan data bukti setor ke database.

```http
POST /api/bukti_setor/save
```

**Request Body:**
```json
{
  "tanggal": "2024-01-15",
  "kode_setor": "411211",
  "jumlah": 100000
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "message": "Data bukti setor berhasil disimpan"
  }
}
```

### 3. Get Bukti Setor History

Mengambil riwayat bukti setor yang telah disimpan.

```http
GET /api/bukti_setor/history
```

**Query Parameters:**
- `bulan` (optional): Filter berdasarkan bulan
- `kode_setor` (optional): Filter berdasarkan kode setor
- `limit` (optional): Limit jumlah data (default: 100)
- `offset` (optional): Offset untuk pagination (default: 0)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "tanggal": "2024-01-15",
      "kode_setor": "411211",
      "jumlah": 100000,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1
}
```

### 4. Export Bukti Setor to Excel

Mengekspor data bukti setor ke format Excel.

```http
GET /api/bukti_setor/export
```

**Query Parameters:**
- `bulan` (optional): Filter berdasarkan bulan
- `kode_setor` (optional): Filter berdasarkan kode setor

**Response:**
Binary Excel file dengan header `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

### 5. Delete Bukti Setor

Menghapus data bukti setor berdasarkan ID.

```http
DELETE /api/bukti_setor/delete/{id}
```

**Path Parameters:**
- `id`: ID bukti setor yang akan dihapus

**Response:**
```json
{
  "success": true,
  "message": "Data bukti setor berhasil dihapus"
}
```

## 🔍 Health Check

### System Health

Mengecek status kesehatan sistem.

```http
GET /api/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "connected",
    "ocr_engine": "ready",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## 📊 Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request berhasil |
| 201 | Created | Data berhasil dibuat |
| 400 | Bad Request | Request tidak valid |
| 404 | Not Found | Data tidak ditemukan |
| 409 | Conflict | Data sudah ada |
| 422 | Unprocessable Entity | Data tidak dapat diproses |
| 500 | Internal Server Error | Error server |

## 🔧 Error Handling

### Common Error Codes

#### 400 - Bad Request
```json
{
  "success": false,
  "error": "Bad Request",
  "details": {
    "field": "jenis",
    "message": "Jenis harus berupa 'masukan' atau 'keluaran'"
  }
}
```

#### 404 - Not Found
```json
{
  "success": false,
  "error": "Not Found",
  "details": {
    "resource": "invoice",
    "id": 123
  }
}
```

#### 500 - Internal Server Error
```json
{
  "success": false,
  "error": "Internal Server Error",
  "details": {
    "message": "Database connection failed"
  }
}
```

## 📝 Data Validation

### Invoice Data Validation

- `no_faktur`: Harus mengikuti format faktur pajak Indonesia
- `tanggal`: Format ISO 8601 (YYYY-MM-DD)
- `npwp_lawan_transaksi`: Format NPWP valid (XX.XXX.XXX.X-XXX.XXX)
- `dpp`: Numeric, minimal 0
- `ppn`: Numeric, minimal 0
- `nama_lawan_transaksi`: String, maksimal 255 karakter
- `keterangan`: String, opsional

### Bukti Setor Data Validation

- `tanggal`: Format ISO 8601 (YYYY-MM-DD)
- `kode_setor`: String, kode setor pajak valid
- `jumlah`: Numeric, minimal 0

## 🚀 Rate Limiting

Untuk production, implementasikan rate limiting:
- 100 requests per minute per IP
- 1000 requests per hour per IP
- File upload: 10 files per minute per IP

## 🔒 Security Headers

Response headers yang direkomendasikan:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy: default-src 'self'`

## 📋 Testing

### Manual Testing dengan cURL

```bash
# Test file upload
curl -X POST \
  http://localhost:5001/api/process \
  -F "file=@test_invoice.pdf" \
  -F "jenis=masukan"

# Test data save
curl -X POST \
  http://localhost:5001/api/save \
  -H "Content-Type: application/json" \
  -d '{"jenis":"masukan","no_faktur":"010.000-24.00000001","tanggal":"2024-01-15","nama_lawan_transaksi":"PT. Test","npwp_lawan_transaksi":"01.234.567.8-901.000","dpp":100000,"ppn":11000}'

# Test history
curl http://localhost:5001/api/history

# Test export
curl -o export.xlsx http://localhost:5001/api/export
```

### Testing dengan Postman

1. Import collection dari file `postman_collection.json`
2. Set environment variables:
   - `base_url`: http://localhost:5001
3. Run tests secara sequence

## 🔄 Pagination

Untuk endpoint yang mendukung pagination:

```http
GET /api/history?limit=10&offset=0
```

Response akan include metadata pagination:
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "current_page": 1,
    "per_page": 10,
    "total": 100,
    "total_pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

## 📊 Performance

### Optimasi Query

- Gunakan indexing pada kolom yang sering di-query
- Implementasikan database connection pooling
- Cache hasil query yang sering diakses

### File Processing

- Batasi ukuran file upload maksimal 16MB
- Implementasikan async processing untuk file besar
- Gunakan background job untuk OCR processing

---

**📞 Support:** Jika ada pertanyaan tentang API, silakan buka issue di GitHub repository.
