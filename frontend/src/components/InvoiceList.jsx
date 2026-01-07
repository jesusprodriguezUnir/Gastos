import { useState, useEffect } from 'react';
import { getInvoices, deleteInvoice } from '../services/api';
import { Trash2, FileText, ExternalLink } from 'lucide-react';

export default function InvoiceList({ refreshTrigger }) {
    const [invoices, setInvoices] = useState([]);
    const [vendorFilter, setVendorFilter] = useState('');

    useEffect(() => {
        loadInvoices();
    }, [refreshTrigger, vendorFilter]);

    const loadInvoices = async () => {
        try {
            const data = await getInvoices(0, 100, vendorFilter);
            setInvoices(data);
        } catch (error) {
            console.error("Error loading invoices", error);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to delete this invoice?")) return;
        try {
            await deleteInvoice(id);
            loadInvoices();
        } catch (error) {
            console.error("Error deleting invoice", error);
        }
    };

    const handleView = (id) => {
        window.open(`http://localhost:8000/api/v1/invoices/${id}/file`, '_blank');
    };

    return (
        <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h3>Invoices</h3>
                <input
                    type="text"
                    placeholder="Filter by Vendor"
                    value={vendorFilter}
                    onChange={(e) => setVendorFilter(e.target.value)}
                    style={{ padding: '0.5rem' }}
                />
            </div>

            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead>
                    <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                        <th style={{ padding: '0.5rem' }}>Date</th>
                        <th style={{ padding: '0.5rem' }}>Vendor</th>
                        <th style={{ padding: '0.5rem' }}>Amount</th>
                        <th style={{ padding: '0.5rem' }}>Category</th>
                        <th style={{ padding: '0.5rem' }}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {invoices.map(inv => (
                        <tr key={inv.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                            <td style={{ padding: '0.5rem' }}>{inv.date}</td>
                            <td style={{ padding: '0.5rem' }}>{inv.vendor}</td>
                            <td style={{ padding: '0.5rem' }}>{inv.amount} {inv.currency}</td>
                            <td style={{ padding: '0.5rem' }}>{inv.category_id}</td>
                            <td style={{ padding: '0.5rem', display: 'flex', gap: '0.5rem' }}>
                                <button onClick={() => handleView(inv.id)} className="btn" title="View File">
                                    <FileText size={16} />
                                </button>
                                <button onClick={() => handleDelete(inv.id)} className="btn" style={{ color: 'var(--color-expense)' }} title="Delete">
                                    <Trash2 size={16} />
                                </button>
                            </td>
                        </tr>
                    ))}
                    {invoices.length === 0 && (
                        <tr>
                            <td colSpan="5" style={{ padding: '1rem', textAlign: 'center' }}>No invoices found.</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
}
