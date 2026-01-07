import { useState, useEffect } from 'react';
import { getTransactions } from '../services/api';
import './Transactions.css';

export default function Transactions() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const res = await getTransactions();
            setData(res);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="transactions-page">
            <div className="card">
                <div className="table-header">
                    <h2>All Transactions</h2>
                    {/* Add filters here */}
                </div>
                <div className="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Description</th>
                                <th>Category</th>
                                <th>Amount</th>
                                <th>Account</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading ? (
                                <tr><td colSpan="5">Loading...</td></tr>
                            ) : data.map((t) => (
                                <tr key={t.id}>
                                    <td>{t.date}</td>
                                    <td>{t.description}</td>
                                    <td>
                                        <span className="badge category">
                                            {t.category ? t.category.name : 'Uncategorized'}
                                        </span>
                                    </td>
                                    <td className={t.amount > 0 ? 'income' : 'expense'}>
                                        {t.amount.toFixed(2)}€
                                    </td>
                                    <td>{t.account ? t.account.name : '-'}</td>
                                </tr>
                            ))}
                            {!loading && data.length === 0 && (
                                <tr><td colSpan="5" style={{ textAlign: 'center' }}>No transactions found</td></tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
