import unittest
import json
from app import app, db
from models import PPNMasukan, PPNKeluaran, BuktiSetor


class TestAPI(unittest.TestCase):
    """Test API endpoints."""
    
    def setUp(self):
        """Set up test database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up test database."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        # Check if it's a proper JSON response
        try:
            data = json.loads(response.data)
            self.assertIn('status', data)
        except json.JSONDecodeError:
            # If it's not JSON, it should at least return OK
            self.assertIn(b'OK', response.data)
    
    def test_save_invoice_masukan(self):
        """Test saving invoice masukan data."""
        invoice_data = {
            'jenis': 'masukan',
            'no_faktur': '010.000-24.00000001',
            'tanggal': '2024-01-15',
            'nama_lawan_transaksi': 'PT. Test Indonesia',
            'npwp_lawan_transaksi': '01.234.567.8-901.000',
            'dpp': 100000,
            'ppn': 11000,
            'keterangan': 'Pembelian barang untuk testing'
        }
        
        response = self.app.post('/api/save',
                                data=json.dumps(invoice_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        # Check if data was saved in database
        saved_invoice = PPNMasukan.query.filter_by(no_faktur='010.000-24.00000001').first()
        self.assertIsNotNone(saved_invoice)
        self.assertEqual(saved_invoice.nama_lawan_transaksi, 'PT. Test Indonesia')
    
    def test_save_invoice_keluaran(self):
        """Test saving invoice keluaran data."""
        invoice_data = {
            'jenis': 'keluaran',
            'no_faktur': '010.000-24.00000002',
            'tanggal': '2024-01-15',
            'nama_lawan_transaksi': 'PT. Test Customer',
            'npwp_lawan_transaksi': '01.234.567.8-901.000',
            'dpp': 200000,
            'ppn': 22000,
            'keterangan': 'Penjualan barang untuk testing'
        }
        
        response = self.app.post('/api/save',
                                data=json.dumps(invoice_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        # Check if data was saved in database
        saved_invoice = PPNKeluaran.query.filter_by(no_faktur='010.000-24.00000002').first()
        self.assertIsNotNone(saved_invoice)
        self.assertEqual(saved_invoice.nama_lawan_transaksi, 'PT. Test Customer')
    
    def test_get_history_empty(self):
        """Test getting history when database is empty."""
        response = self.app.get('/api/history')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
    
    def test_get_history_with_data(self):
        """Test getting history with data."""
        # Add sample data
        ppn = PPNMasukan(
            bulan='Januari',
            tanggal='2024-01-15',
            keterangan='Test pembelian',
            npwp_lawan_transaksi='01.234.567.8-901.000',
            nama_lawan_transaksi='PT. Test',
            no_faktur='010.000-24.00000001',
            dpp=100000,
            ppn=11000
        )
        db.session.add(ppn)
        db.session.commit()
        
        response = self.app.get('/api/history')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['no_faktur'], '010.000-24.00000001')
    
    def test_bukti_setor_save(self):
        """Test saving bukti setor data."""
        bukti_data = {
            'tanggal': '2024-01-15',
            'kode_setor': '411211',
            'jumlah': 100000
        }
        
        response = self.app.post('/api/bukti_setor/save',
                                data=json.dumps(bukti_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        # Check if data was saved in database
        saved_bukti = BuktiSetor.query.filter_by(kode_setor='411211').first()
        self.assertIsNotNone(saved_bukti)
        self.assertEqual(saved_bukti.jumlah, 100000)
    
    def test_bukti_setor_history_empty(self):
        """Test getting bukti setor history when database is empty."""
        response = self.app.get('/api/bukti_setor/history')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
    
    def test_bukti_setor_history_with_data(self):
        """Test getting bukti setor history with data."""
        # Add sample data
        bukti = BuktiSetor(
            tanggal='2024-01-15',
            kode_setor='411211',
            jumlah=100000
        )
        db.session.add(bukti)
        db.session.commit()
        
        response = self.app.get('/api/bukti_setor/history')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['kode_setor'], '411211')
    
    def test_invalid_jenis_save(self):
        """Test saving invoice with invalid jenis."""
        invoice_data = {
            'jenis': 'invalid_jenis',
            'no_faktur': '010.000-24.00000001',
            'tanggal': '2024-01-15',
            'nama_lawan_transaksi': 'PT. Test Indonesia',
            'npwp_lawan_transaksi': '01.234.567.8-901.000',
            'dpp': 100000,
            'ppn': 11000,
            'keterangan': 'Pembelian barang untuk testing'
        }
        
        response = self.app.post('/api/save',
                                data=json.dumps(invoice_data),
                                content_type='application/json')
        
        # Should return an error
        self.assertEqual(response.status_code, 400)
    
    def test_missing_required_fields(self):
        """Test saving invoice with missing required fields."""
        invoice_data = {
            'jenis': 'masukan',
            # Missing no_faktur
            'tanggal': '2024-01-15',
            'nama_lawan_transaksi': 'PT. Test Indonesia',
        }
        
        response = self.app.post('/api/save',
                                data=json.dumps(invoice_data),
                                content_type='application/json')
        
        # Should return an error
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
