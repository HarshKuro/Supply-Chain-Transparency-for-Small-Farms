// js/auth.js
import { auth, db } from './firebase-config.js';
import { 
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword, 
    signOut,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { 
    doc, 
    setDoc, 
    getDoc, 
    serverTimestamp 
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { showLoader, hideLoader, showAlert } from './common.js';

// Route map for roles
export const roleRoutes = {
    'farmer': 'farmer/dashboard.html',
    'wholesaler': 'wholesaler/dashboard.html',
    'driver': 'driver/dashboard.html',
    'customer': 'customer/dashboard.html',
    'admin': 'admin/dashboard.html'
};

// Register User
export async function registerUser(fullName, email, password, phone, role) {
    showLoader();
    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Save additional user info in Firestore
        await setDoc(doc(db, "users", user.uid), {
            name: fullName,
            email: email,
            phone: phone,
            role: role,
            createdAt: serverTimestamp()
        });

        showAlert("Registration successful!", "success");
        // Redirect to dashboard
        window.location.href = getBaseUrl() + roleRoutes[role];
    } catch (error) {
        console.error("Error registering:", error);
        showAlert(error.message, "error");
    } finally {
        hideLoader();
    }
}

// Login User
export async function loginUser(email, password) {
    showLoader();
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        
        // Fetch role from Firestore
        const userDoc = await getDoc(doc(db, "users", user.uid));
        
        if (userDoc.exists()) {
            const role = userDoc.data().role;
            showAlert("Login successful!", "success");
            window.location.href = getBaseUrl() + roleRoutes[role];
        } else {
            showAlert("User record not found.", "error");
            await signOut(auth);
        }
    } catch (error) {
        console.error("Error logging in:", error);
        showAlert("Invalid email or password.", "error");
    } finally {
        hideLoader();
    }
}

// Logout User
export async function logoutUser() {
    showLoader();
    try {
        await signOut(auth);
        window.location.href = getBaseUrl() + 'login.html';
    } catch (error) {
        console.error("Error logging out:", error);
        showAlert(error.message, "error");
    } finally {
        hideLoader();
    }
}

// Check role access
export function checkRoleAccess(requiredRole) {
    showLoader();
    onAuthStateChanged(auth, async (user) => {
        if (user) {
            try {
                const userDoc = await getDoc(doc(db, "users", user.uid));
                if (userDoc.exists()) {
                    const role = userDoc.data().role;
                    if (role !== requiredRole && requiredRole !== 'any') {
                        // Redirect to appropriate dashboard
                        window.location.href = getBaseUrl() + roleRoutes[role];
                    } else {
                        // User is authorized
                        hideLoader();
                    }
                } else {
                    window.location.href = getBaseUrl() + 'login.html';
                }
            } catch (error) {
                console.error("Error verifying role:", error);
                window.location.href = getBaseUrl() + 'login.html';
            }
        } else {
            // Not logged in
            window.location.href = getBaseUrl() + 'login.html';
        }
    });
}

// Get user data globally
export function getCurrentUserData(callback) {
    onAuthStateChanged(auth, async (user) => {
        if (user) {
            const userDoc = await getDoc(doc(db, "users", user.uid));
            if (userDoc.exists()) {
                callback({ id: user.uid, ...userDoc.data() });
            } else {
                callback(null);
            }
        } else {
            callback(null);
        }
    });
}

// Helper to get base url
function getBaseUrl() {
    // If we are in a subdirectory like 'farmer/dashboard.html', we need to go up
    const path = window.location.pathname;
    if (path.includes('/farmer/') || path.includes('/wholesaler/') || path.includes('/driver/') || path.includes('/customer/') || path.includes('/admin/')) {
        return '../';
    }
    return '';
}
