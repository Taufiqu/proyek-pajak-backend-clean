import pytest
from app import app, db
from models import PPNMasukan, PPNKeluaran, BuktiSetor


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture
def app_context():
    """Create an application context for testing."""
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def sample_invoice_data():
    """Sample invoice data for testing."""
    return {
        'jenis': 'masukan',
        'no_faktur': '010.000-24.00000001',
        'tanggal': '2024-01-15',
        'nama_lawan_transaksi': 'PT. Test Indonesia',
        'npwp_lawan_transaksi': '01.234.567.8-901.000',
        'dpp': 100000,
        'ppn': 11000,
        'keterangan': 'Pembelian barang untuk testing'
    }


@pytest.fixture
def sample_bukti_setor_data():
    """Sample bukti setor data for testing."""
    return {
        'tanggal': '2024-01-15',
        'kode_setor': '411211',
        'jumlah': 100000
    }


@pytest.fixture
def sample_ppn_masukan(app_context):
    """Create a sample PPNMasukan record."""
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
    return ppn


@pytest.fixture
def sample_ppn_keluaran(app_context):
    """Create a sample PPNKeluaran record."""
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
    return ppn


@pytest.fixture
def sample_bukti_setor(app_context):
    """Create a sample BuktiSetor record."""
    bukti = BuktiSetor(
        tanggal='2024-01-15',
        kode_setor='411211',
        jumlah=100000
    )
    db.session.add(bukti)
    db.session.commit()
    return bukti
