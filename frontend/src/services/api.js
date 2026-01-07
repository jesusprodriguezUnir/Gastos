import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getTransactions = async (skip = 0, limit = 100) => {
    const response = await api.get(`/transactions/?skip=${skip}&limit=${limit}`);
    return response.data;
};

export const getAccounts = async () => {
    const response = await api.get('/accounts/');
    return response.data;
};

export const getCategories = async () => {
    const response = await api.get('/categories/');
    return response.data;
};

export const uploadBankFile = async (file, bankName, accountId) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('bank_name', bankName);
    formData.append('account_id', accountId);

    const response = await api.post('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const getInvoices = async (skip = 0, limit = 100, vendor = '', category_id = '') => {
    let query = `/invoices/?skip=${skip}&limit=${limit}`;
    if (vendor) query += `&vendor=${vendor}`;
    if (category_id) query += `&category_id=${category_id}`;
    const response = await api.get(query);
    return response.data;
};

export const getInvoiceCategories = async () => {
    const response = await api.get('/invoices/categories/');
    return response.data;
};

export const uploadInvoice = async (formData) => {
    const response = await api.post('/invoices/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const deleteInvoice = async (id) => {
    const response = await api.delete(`/invoices/${id}`);
    return response.data;
};

export default api;
