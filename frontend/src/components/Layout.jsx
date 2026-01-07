import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, Receipt, Import, CreditCard } from 'lucide-react';
import './Layout.css';

export default function Layout() {
    return (
        <div className="layout">
            <aside className="sidebar">
                <div className="logo">
                    <h2>FinanceFlow</h2>
                </div>
                <nav>
                    <NavLink to="/" end className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                        <LayoutDashboard size={20} />
                        <span>Dashboard</span>
                    </NavLink>
                    <NavLink to="/transactions" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                        <Receipt size={20} />
                        <span>Transactions</span>
                    </NavLink>
                    <NavLink to="/import" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                        <Import size={20} />
                        <span>Import</span>
                    </NavLink>
                </nav>
            </aside >
            <main className="content">
                <header className="topbar">
                    <div className="breadcrumbs">Welcome back</div>
                    <div className="user-profile">
                        <div className="avatar">JD</div>
                    </div>
                </header>
                <div className="page-content">
                    <Outlet />
                </div>
            </main>
        </div >
    );
}
