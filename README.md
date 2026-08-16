# Supply Chain Transparency for Small Farms
**Enhancing Fair Trade Through Digital Traceability**

## Project Overview
This is a simple web-based supply chain management platform connecting Farmers, Wholesalers, Drivers, Customers, and Administrators. It tracks agricultural products from listing to delivery and feedback.

## Features
- **Product Management:** Farmers can list and manage their produce.
- **Order Tracking:** Customers place orders and track their status.
- **Inventory Management:** Stock automatically decreases when orders are placed.
- **Delivery Status:** Drivers update order status across the delivery lifecycle.
- **Role-Based Access:** Dedicated dashboards for Farmer, Wholesaler, Driver, Customer, and Admin.
- **Customer Feedback:** Customers can rate and comment on delivered orders.

## Technology Stack
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Firebase Authentication, Cloud Firestore
- **Tools:** VS Code, Live Server

## Folder Structure
```text
├── index.html
├── login.html
├── register.html
├── README.md
├── FIREBASE_SETUP.md
├── TESTING.md
├── firestore.rules
├── css/
│   ├── style.css
│   ├── auth.css
│   └── dashboard.css
├── js/
│   ├── firebase-config.js
│   ├── auth.js
│   ├── common.js
│   ├── farmer.js
│   ├── wholesaler.js
│   ├── driver.js
│   ├── customer.js
│   └── admin.js
├── farmer/
├── wholesaler/
├── driver/
├── customer/
└── admin/
```

## Running Locally
1. Install **VS Code**.
2. Install the **Live Server** extension in VS Code.
3. Open the project folder in VS Code.
4. Right-click on `index.html` and select **"Open with Live Server"**.

## Firebase Setup
To connect this project to your own database, you must set up Firebase. See [FIREBASE_SETUP.md](./FIREBASE_SETUP.md) for detailed instructions.

## Deployment
This project consists entirely of static files (HTML, CSS, JS). You can easily deploy it using **GitHub Pages**, **Vercel**, or **Firebase Hosting**.
