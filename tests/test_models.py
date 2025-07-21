import unittest
from app import app, db
from models import PPNMasukan, PPNKeluaran, BuktiSetor


class TestModels(unittest.TestCase):
    """Test database models."""
    
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
    
    def test_ppn_masukan_creation(self):
        """Test PPNMasukan model creation."""
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
        
        self.assertIsNotNone(ppn.id)
        self.assertEqual(ppn.no_faktur, '010.000-24.00000001')
        self.assertEqual(ppn.dpp, 100000)
        self.assertEqual(ppn.ppn, 11000)
    
    def test_ppn_keluaran_creation(self):
        """Test PPNKeluaran model creation."""
        ppn = PPNKeluaran(
            bulan='Januari',
            tanggal='2024-01-15',
            keterangan='Test penjualan',
            npwp_lawan_transaksi='01.234.567.8-901.000',
            nama_lawan_transaksi='PT. Test',
            no_faktur='010.000-24.00000002',
            dpp=200000,
            ppn=22000
        )
        db.session.add(ppn)
        db.session.commit()
        
        self.assertIsNotNone(ppn.id)
        self.assertEqual(ppn.no_faktur, '010.000-24.00000002')
        self.assertEqual(ppn.dpp, 200000)
        self.assertEqual(ppn.ppn, 22000)
    
    def test_bukti_setor_creation(self):
        """Test BuktiSetor model creation."""
        bukti = BuktiSetor(
            tanggal='2024-01-15',
            kode_setor='411211',
            jumlah=100000
        )
        db.session.add(bukti)
        db.session.commit()
        
        self.assertIsNotNone(bukti.id)
        self.assertEqual(bukti.kode_setor, '411211')
        self.assertEqual(bukti.jumlah, 100000)
    
    def test_ppn_masukan_unique_no_faktur(self):
        """Test PPNMasukan unique constraint on no_faktur."""
        # Create first record
        ppn1 = PPNMasukan(
            bulan='Januari',
            tanggal='2024-01-15',
            keterangan='Test pembelian 1',
            npwp_lawan_transaksi='01.234.567.8-901.000',
            nama_lawan_transaksi='PT. Test',
            no_faktur='010.000-24.00000001',
            dpp=100000,
            ppn=11000
        )
        db.session.add(ppn1)
        db.session.commit()
        
        # Try to create second record with same no_faktur
        ppn2 = PPNMasukan(
            bulan='Januari',
            tanggal='2024-01-15',
            keterangan='Test pembelian 2',
            npwp_lawan_transaksi='01.234.567.8-901.000',
            nama_lawan_transaksi='PT. Test',
            no_faktur='010.000-24.00000001',  # Same no_faktur
            dpp=100000,
            ppn=11000
        )
        db.session.add(ppn2)
        
        # This should raise an IntegrityError
        with self.assertRaises(Exception):
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
