import requests
import os

API_URL = "http://localhost:8000/api/v1/invoices"
TEST_FILE = "test_invoice.txt"

def test_invoice_flow():
    # 1. Create a dummy file
    with open(TEST_FILE, "w") as f:
        f.write("Dummy invoice content")

    try:
        # 2. Upload Invoice
        print("Uploading invoice...")
        with open(TEST_FILE, "rb") as f:
            files = {"file": (TEST_FILE, f, "text/plain")}
            data = {
                "vendor": "Test Vendor",
                "date": "2023-10-27",
                "amount": "123.45",
                "currency": "EUR",
                "description": "Test Invoice Description"
            }
            response = requests.post(f"{API_URL}/upload", files=files, data=data)
        
        if response.status_code != 200:
            print(f"Upload failed: {response.text}")
            return
        
        invoice = response.json()
        invoice_id = invoice["id"]
        print(f"Invoice uploaded with ID: {invoice_id}")

        # 3. List Invoices
        print("Listing invoices...")
        response = requests.get(API_URL)
        invoices = response.json()
        print(f"Found {len(invoices)} invoices.")
        found = any(i["id"] == invoice_id for i in invoices)
        if found:
            print("Uploaded invoice found in list.")
        else:
            print("ERROR: Uploaded invoice NOT found in list.")

        # 4. Get Invoice Details
        print(f"Getting invoice details for ID {invoice_id}...")
        response = requests.get(f"{API_URL}/{invoice_id}")
        if response.status_code == 200:
            print("Invoice details retrieved successfully.")
        else:
            print(f"Failed to get details: {response.text}")

        # 5. Delete Invoice
        print(f"Deleting invoice ID {invoice_id}...")
        response = requests.delete(f"{API_URL}/{invoice_id}")
        if response.status_code == 200:
            print("Invoice deleted successfully.")
        else:
            print(f"Failed to delete: {response.text}")

        # 6. Verify Deletion
        response = requests.get(f"{API_URL}/{invoice_id}")
        if response.status_code == 404:
            print("Verification: Invoice correctly returned 404 after deletion.")
        else:
            print(f"ERROR: Invoice still exists or error: {response.status_code}")

    finally:
        # Cleanup
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

if __name__ == "__main__":
    test_invoice_flow()
