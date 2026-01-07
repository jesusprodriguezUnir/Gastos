import React, { useState, useEffect } from 'react';
import { getInvoices, getInvoiceCategories, uploadInvoice, deleteInvoice } from '../services/api';
import { Plus, Trash, FileText, Droplet, Zap, Flame, Wifi, Home, Shield, Clipboard, CreditCard } from 'lucide-react';
import './Invoices.css';

const iconMap = {
    'droplet': Droplet,
    'zap': Zap,
    'flame': Flame,
    'wifi': Wifi,
    'building': Home,
    'shield': Shield,
    'file-text': Clipboard,
    'banknote': CreditCard
};

export default function Invoices() {
    const [invoices, setInvoices] = useState([]);
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);

    // Form State
    const [vendor, setVendor] = useState('');
    const [amount, setAmount] = useState('');
    const [date, setDate] = useState('');
    const [categoryId, setCategoryId] = useState('');
    const [file, setFile] = useState(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [invMsg, catMsg] = await Promise.all([
                getInvoices(0, 1000),
                getInvoiceCategories()
            ]);
            setInvoices(invMsg);
            setCategories(catMsg);
        } catch (error) {
            console.error("Error loading invoices", error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('vendor', vendor);
        formData.append('date', date);
        formData.append('amount', amount);
        formData.append('invoice_category_id', categoryId);
        formData.append('file', file);

        try {
            await uploadInvoice(formData);
            setShowModal(false);
            loadData();
            // Reset form
            setVendor(''); setAmount(''); setDate(''); setCategoryId(''); setFile(null);
        } catch (error) {
            alert('Error uploading invoice');
            console.error(error);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Delete this invoice?')) {
            await deleteInvoice(id);
            loadData();
        }
    };

    // Group invoices by category
    const groupedInvoices = categories.map(cat => {
        return {
            ...cat,
            invoices: invoices.filter(inv => inv.invoice_category_id === cat.id)
        };
    });

    // Add "Uncategorized" group if any
    const uncategorized = invoices.filter(inv => !inv.invoice_category_id);
    if (uncategorized.length > 0) {
        groupedInvoices.push({ id: null, name: 'Sin Categoría', icon: 'file-text', invoices: uncategorized });
    }

    if (loading) return <div style={{ padding: '2rem' }}>Loading...</div>;

    return (
        <div className="invoices-page">
            <div className="invoices-header">
                <h1>Facturas</h1>
                <button
                    onClick={() => setShowModal(true)}
                    className="btn btn-primary"
                >
                    <Plus size={20} /> Nueva Factura
                </button>
            </div>

            <div className="invoices-grid">
                {groupedInvoices.map((group) => (
                    <div key={group.id || 'uncat'} className="card category-card">
                        <div className="category-header">
                            {(() => {
                                const IconComp = iconMap[group.icon] || FileText;
                                return <IconComp className="category-icon" size={24} />;
                            })()}
                            <h2 className="category-title">{group.name}</h2>
                            <span className="category-count">
                                {group.invoices.length}
                            </span>
                        </div>

                        <div className="invoice-list custom-scrollbar">
                            {group.invoices.length === 0 ? (
                                <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic', fontSize: '0.9rem' }}>
                                    No hay facturas.
                                </p>
                            ) : (
                                group.invoices.map(inv => (
                                    <div key={inv.id} className="invoice-item">
                                        <div className="invoice-info">
                                            <h3>{inv.vendor}</h3>
                                            <p className="invoice-date">{inv.date}</p>
                                        </div>
                                        <div style={{ display: 'flex', alignItems: 'center' }}>
                                            <span className="invoice-amount">{inv.amount} €</span>
                                            <button
                                                onClick={() => handleDelete(inv.id)}
                                                className="btn-delete"
                                                title="Eliminar"
                                            >
                                                <Trash size={16} />
                                            </button>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Modal */}
            {showModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>Subir Factura</h2>
                        <form onSubmit={handleUpload}>
                            <div className="form-group">
                                <label>Proveedor / Concepto</label>
                                <input type="text" className="form-input" required
                                    value={vendor} onChange={e => setVendor(e.target.value)} placeholder="Ej. Iberdrola" />
                            </div>
                            <div className="form-row">
                                <div className="form-group">
                                    <label>Fecha</label>
                                    <input type="date" className="form-input" required
                                        value={date} onChange={e => setDate(e.target.value)} />
                                </div>
                                <div className="form-group">
                                    <label>Importe (€)</label>
                                    <input type="number" step="0.01" className="form-input" required
                                        value={amount} onChange={e => setAmount(e.target.value)} />
                                </div>
                            </div>
                            <div className="form-group">
                                <label>Categoría</label>
                                <select className="form-input" required
                                    value={categoryId} onChange={e => setCategoryId(e.target.value)}
                                >
                                    <option value="">Selecciona una...</option>
                                    {categories.map(cat => (
                                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="form-group">
                                <label>Archivo de Factura</label>
                                <input type="file" className="form-input" required
                                    onChange={e => setFile(e.target.files[0])} />
                            </div>
                            <div className="modal-actions">
                                <button type="button" onClick={() => setShowModal(false)} className="btn" style={{ background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-primary)' }}>Cancelar</button>
                                <button type="submit" className="btn btn-primary">Guardar</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
