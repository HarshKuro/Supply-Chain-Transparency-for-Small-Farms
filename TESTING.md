# Testing Guide

Use this guide to verify the complete workflow of the Supply Chain Transparency project.

## Test Cases

| Test Case | Steps to Test | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| **Register User** | Click Register. Fill form. | Account created, redirected to correct dashboard. | Pending |
| **Login User** | Click Login. Enter credentials. | Successfully logs in to appropriate dashboard. | Pending |
| **Role Protection** | As Farmer, try opening `admin/dashboard.html` | Redirected to Farmer dashboard or login. | Pending |
| **Add Product** | Log in as Farmer. Add Tomato, 100kg. | Product appears in My Products list. | Pending |
| **Edit Product** | As Farmer, change price of Tomato. | Price updates successfully. | Pending |
| **Add to Cart** | Log in as Customer. Add Tomato to Cart. | Cart count increases. Item appears in cart. | Pending |
| **Place Order** | As Customer, go to Cart, place order. | Order created, cart clears, stock decreases. | Pending |
| **Insufficient Stock** | Try ordering more quantity than available. | Error message shown. Order blocked. | Pending |
| **Confirm Order** | Log in as Farmer. View Orders. Click Confirm. | Status changes to "Confirmed". | Pending |
| **Verify Order** | Log in as Wholesaler. Click Verify Stock. | Status changes to "Verified". | Pending |
| **Driver Updates** | Log in as Driver. Accept delivery. | Status changes to "Assigned". | Pending |
| **Driver Transit** | Driver clicks Picked Up, then In Transit. | Status updates accordingly. | Pending |
| **Delivery** | Driver clicks Mark Delivered. | Status changes to "Delivered". | Pending |
| **Order Tracking** | Log in as Customer. View My Orders. | Tracker shows current status accurately. | Pending |
| **Submit Feedback** | As Customer, click Give Feedback on delivered order. | Feedback is saved successfully. | Pending |
| **Admin Overview** | Log in as Admin. View Users, Products, Orders. | All platform data is visible. | Pending |
| **Admin Delete** | As Admin, delete a product or user record. | Item is removed from Firestore. | Pending |

## Execution
Run through each scenario chronologically to ensure the end-to-end workflow functions properly.
