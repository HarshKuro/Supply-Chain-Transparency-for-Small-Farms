# Firebase Setup Guide

Follow these steps to set up Firebase for the Supply Chain Transparency project.

## 1. Create a Firebase Project
1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Click **"Add project"**.
3. Name your project (e.g., "Supply Chain Project").
4. Disable Google Analytics (not needed for this academic project).
5. Click **"Create project"**.

## 2. Enable Authentication
1. In your Firebase dashboard, click **"Authentication"** (under Build).
2. Click **"Get started"**.
3. Under the **"Sign-in method"** tab, click **"Email/Password"**.
4. Enable the first toggle (Email/Password) and click **"Save"**.

## 3. Create Firestore Database
1. In the left menu, click **"Firestore Database"** (under Build).
2. Click **"Create database"**.
3. Select a location closest to you and click **"Next"**.
4. Start in **"Test mode"** and click **"Enable"**.

## 4. Get Firebase Configuration
1. Go to **Project Overview** (click the gear icon next to it and select **Project settings**).
2. Scroll down to the **"Your apps"** section.
3. Click the **Web** icon (`</>`).
4. Register the app with a nickname.
5. Copy the `firebaseConfig` object from the provided code snippet.
6. Open `js/firebase-config.js` in this project.
7. Replace the placeholder `firebaseConfig` with your actual config.

## 5. Add Firestore Security Rules
1. In the Firebase Console, go to **Firestore Database**.
2. Click the **"Rules"** tab.
3. Copy the contents of the `firestore.rules` file in this project.
4. Paste them into the Rules editor in Firebase and click **"Publish"**.

## 6. Create Demo Accounts
Open the running web app (via Live Server) and register these demo accounts:
- farmer@example.com (Role: Farmer)
- wholesaler@example.com (Role: Wholesaler)
- driver@example.com (Role: Driver)
- customer@example.com (Role: Customer)

## 7. Create an Admin Account
Since the UI doesn't allow registering as Admin:
1. Register a user as `admin@example.com` with the "Customer" role through the UI.
2. Go to the Firebase Console -> Firestore Database.
3. Open the `users` collection.
4. Find the document for `admin@example.com`.
5. Change the `role` field from `"customer"` to `"admin"`.

## 8. Add Sample Data
1. Log in as the Farmer (`farmer@example.com`).
2. Add products like Tomato, Potato, Onion with prices and quantities.
3. Log out, then log in as the Customer to test the workflow.
