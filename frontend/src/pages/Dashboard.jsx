import { useEffect, useState } from 'react';
import { getTransactions } from '../services/api'; // In real app, fetch stats
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title } from 'chart.js';
import { Doughnut, Line } from 'react-chartjs-2';
import './Dashboard.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title);

export default function Dashboard() {
    const [transactions, setTransactions] = useState([]);
    const [stats, setStats] = useState({ income: 0, expense: 0, balance: 0 });

    useEffect(() => {
        // Basic stats calculation on client side for MVP
        getTransactions(0, 500).then(data => {
            setTransactions(data);
            let income = 0;
            let expense = 0;
            data.forEach(t => {
                // Simple logic: positive amount = income? 
                // Or check category type. Assume amount sign for now if db stores signed values.
                // If imports are positive, we need logic. usually expense is negative.
                if (t.amount > 0) income += t.amount;
                else expense += Math.abs(t.amount);
            });
            setStats({ income, expense, balance: income - expense });
        }).catch(err => console.error(err));
    }, []);

    const chartData = {
        labels: ['Income', 'Expense'],
        datasets: [
            {
                data: [stats.income, stats.expense],
                backgroundColor: ['#10b981', '#ef4444'],
                borderWidth: 0,
            },
        ],
    };

    return (
        <div className="dashboard">
            <div className="stats-grid">
                <div className="card stat-card">
                    <h3>Total Balance</h3>
                    <p className="amount">€{stats.balance.toFixed(2)}</p>
                </div>
                <div className="card stat-card">
                    <h3>Income</h3>
                    <p className="amount income">+€{stats.income.toFixed(2)}</p>
                </div>
                <div className="card stat-card">
                    <h3>Expenses</h3>
                    <p className="amount expense">-€{stats.expense.toFixed(2)}</p>
                </div>
            </div>

            <div className="charts-grid">
                <div className="card chart-card">
                    <h3>Cash Flow</h3>
                    <div className="chart-container">
                        <Doughnut data={chartData} options={{ maintainAspectRatio: false }} />
                    </div>
                </div>
                <div className="card chart-card">
                    <h3>Recent Transactions</h3>
                    <ul className="recent-list">
                        {transactions.slice(0, 5).map(t => (
                            <li key={t.id}>
                                <span>{t.description}</span>
                                <span className={t.amount > 0 ? 'income' : 'expense'}>
                                    {t.amount > 0 ? '+' : ''}{t.amount}€
                                </span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}
