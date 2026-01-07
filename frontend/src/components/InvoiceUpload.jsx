import { useState, useEffect } from 'react';
import { uploadInvoice, getCategories } from '../services/api';

export default function InvoiceUpload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [vendor, setVendor] = useState('');
    const [date, setDate] = useState('');
    const [amount, setAmount] = useState('');
    const [currency, setCurrency] = useState('EUR');
    const [description, setDescription] = useState('');
    const [categoryId, setCategoryId] = useState('');
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        loadCategories();
    }, []);

    const loadCategories = async () => {
        try {
            const data = await getCategories();
            setCategories(data);
        } catch (error) {
            console.error("Error loading categories", error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file || !vendor || !date || !amount) {
            setMessage('Please fill in all required fields.');
            return;
        }

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append('vendor', vendor);
        formData.append('date', date);
        formData.append('amount', amount);
        formData.append('currency', currency);
        formData.append('description', description);
        if (categoryId) formData.append('category_id', categoryId);

        try {
            await uploadInvoice(formData);
            setMessage('Invoice uploaded successfully!');
            // Reset form
            setFile(null);
            setVendor('');
            setDate('');
            setAmount('');
            setDescription('');
            setCategoryId('');
            if (onUploadSuccess) onUploadSuccess();
        } catch (error) {
            console.error(error);
            setMessage('Error uploading invoice.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card">
            <h3>Upload Invoice</h3>
            {message && <p>{message}</p>}
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files[0])}
                    accept="application/pdf,image/*"
                    required
                />
                <input
                    type="text"
                    placeholder="Vendor"
                    value={vendor}
                    onChange={(e) => setVendor(e.target.value)}
                    required
                    style={{ padding: '0.5rem' }}
                />
                <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    required
                    style={{ padding: '0.5rem' }}
                />
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <input
                        type="number"
                        step="0.01"
                        placeholder="Amount"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        required
                        style={{ padding: '0.5rem', flex: 1 }}
                    />
                    <select
                        value={currency}
                        onChange={(e) => setCurrency(e.target.value)}
                        style={{ padding: '0.5rem' }}
                    >
                        <option value="EUR">EUR</option>
                        <option value="USD">USD</option>
                    </select>
                </div>
                <select
                    value={categoryId}
                    onChange={(e) => setCategoryId(e.target.value)}
                    style={{ padding: '0.5rem' }}
                >
                    <option value="">Select Category</option>
                    {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                </select>
                <textarea
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    style={{ padding: '0.5rem' }}
                />
                <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Uploading...' : 'Upload'}
                </button>
            </form>
        </div>
    );
}
