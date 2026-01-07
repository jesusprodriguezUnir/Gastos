import { useState, useEffect } from 'react';
import { uploadBankFile, getAccounts } from '../services/api';
import './Import.css';
import { UploadCloud, CheckCircle, AlertCircle } from 'lucide-react';

export default function ImportData() {
    const [file, setFile] = useState(null);
    const [bank, setBank] = useState('CAIXA');
    const [accountId, setAccountId] = useState('');
    const [accounts, setAccounts] = useState([]);
    const [status, setStatus] = useState('idle'); // idle, uploading, success, error
    const [message, setMessage] = useState('');

    useEffect(() => {
        getAccounts().then(setAccounts).catch(console.error);
    }, []);

    const handleFileChange = (e) => {
        if (e.target.files) setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file || !accountId) return;
        setStatus('uploading');
        try {
            const res = await uploadBankFile(file, bank, accountId);
            setStatus('success');
            setMessage(`Successfully imported ${res.count} transactions.`);
        } catch (err) {
            setStatus('error');
            setMessage('Failed to upload file. Check format.');
            console.error(err);
        }
    };

    return (
        <div className="import-page">
            <div className="card import-card">
                <h2>Import Bank Statements</h2>
                <p className="subtitle">Upload Excel or CSV files from your bank.</p>

                <div className="form-group">
                    <label>Select Bank</label>
                    <select value={bank} onChange={(e) => setBank(e.target.value)}>
                        <option value="CAIXA">CaixaBank</option>
                        <option value="ING">ING</option>
                        <option value="SABADELL">Sabadell</option>
                        <option value="REVOLUT">Revolut</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Target Account</label>
                    <select value={accountId} onChange={(e) => setAccountId(e.target.value)}>
                        <option value="">Select an Account</option>
                        {accounts.map(acc => (
                            <option key={acc.id} value={acc.id}>{acc.name} ({acc.bank_name})</option>
                        ))}
                    </select>
                </div>

                <div className="dropzone">
                    <input type="file" id="file-upload" onChange={handleFileChange} />
                    <label htmlFor="file-upload" className="dropzone-label">
                        <UploadCloud size={48} />
                        <span>{file ? file.name : "Click to upload or drag and drop"}</span>
                    </label>
                </div>

                <button
                    className="btn btn-primary upload-btn"
                    disabled={!file || !accountId || status === 'uploading'}
                    onClick={handleUpload}
                >
                    {status === 'uploading' ? 'Processing...' : 'Start Import'}
                </button>

                {status === 'success' && (
                    <div className="alert success">
                        <CheckCircle size={20} /> {message}
                    </div>
                )}
                {status === 'error' && (
                    <div className="alert error">
                        <AlertCircle size={20} /> {message}
                    </div>
                )}
            </div>
        </div>
    );
}
