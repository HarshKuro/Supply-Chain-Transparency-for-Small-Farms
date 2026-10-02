// js/navbar.js - Reusable Universal Navbar Component

// Guaranteed self-contained CSS to protect against any stylesheet caching or layout conflicts
function injectNavbarStyles() {
    if (document.getElementById('app-navbar-injected-styles')) return;

    const style = document.createElement('style');
    style.id = 'app-navbar-injected-styles';
    style.textContent = `
        .app-navbar {
            display: block !important;
            position: sticky !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            z-index: 99999 !important;
            background: #ffffff !important;
            border-bottom: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
            padding: 0 !important;
            margin: 0 !important;
            height: 68px !important;
            box-sizing: border-box !important;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
        }

        .app-navbar .navbar-inner {
            display: flex !important;
            flex-direction: row !important;
            justify-content: space-between !important;
            align-items: center !important;
            width: 100% !important;
            height: 100% !important;
            padding: 0 2rem !important;
            margin: 0 auto !important;
            box-sizing: border-box !important;
        }

        .app-navbar.public-mode .navbar-inner {
            max-width: 1280px !important;
            padding: 0 1.5rem !important;
        }

        .app-navbar .brand {
            display: inline-flex !important;
            flex-direction: row !important;
            align-items: center !important;
            gap: 0.75rem !important;
            text-decoration: none !important;
            color: #0f172a !important;
            font-size: 1.25rem !important;
            font-weight: 800 !important;
            white-space: nowrap !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .app-navbar .brand-icon {
            width: 36px !important;
            height: 36px !important;
            background: linear-gradient(135deg, #10b981, #047857) !important;
            border-radius: 10px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1.2rem !important;
            color: #ffffff !important;
            flex-shrink: 0 !important;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.25) !important;
        }

        .app-navbar .role-tag {
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.04em !important;
            padding: 0.25rem 0.65rem !important;
            border-radius: 9999px !important;
            text-transform: uppercase !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.35rem !important;
            margin-left: 0.5rem !important;
            white-space: nowrap !important;
        }

        .app-navbar .nav-links-group {
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            gap: 0.5rem !important;
            margin: 0 !important;
            padding: 0 !important;
            list-style: none !important;
        }

        .app-navbar .nav-links-group a {
            color: #475569 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: 0.5rem 0.9rem !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            transition: all 0.2s ease !important;
            white-space: nowrap !important;
        }

        .app-navbar .nav-links-group a:hover {
            color: #059669 !important;
            background: rgba(16, 185, 129, 0.08) !important;
        }

        .app-navbar .nav-right-group {
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            gap: 0.85rem !important;
            white-space: nowrap !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .app-navbar .user-info {
            display: inline-flex !important;
            flex-direction: row !important;
            align-items: center !important;
            gap: 0.85rem !important;
        }

        .app-navbar .user-info #userName {
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            color: #1e293b !important;
            background: #f1f5f9 !important;
            padding: 0.4rem 0.9rem !important;
            border-radius: 9999px !important;
            border: 1px solid #e2e8f0 !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.4rem !important;
            white-space: nowrap !important;
        }

        .app-navbar #logoutBtn {
            background: #fff1f2 !important;
            color: #e11d48 !important;
            border: 1px solid #ffe4e6 !important;
            font-size: 0.85rem !important;
            padding: 0.45rem 1rem !important;
            border-radius: 9999px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            white-space: nowrap !important;
            display: inline-flex !important;
            align-items: center !important;
        }

        .app-navbar #logoutBtn:hover {
            background: #ffe4e6 !important;
            color: #be123c !important;
            transform: translateY(-1px) !important;
        }

        @media (max-width: 820px) {
            .app-navbar .nav-links-group {
                display: none !important;
            }
            .app-navbar .navbar-inner {
                padding: 0 1rem !important;
            }
        }
    `;
    document.head.appendChild(style);
}

/**
 * Universal Navbar Component for AgriTrace
 */
export function initNavbar(options = {}) {
    injectNavbarStyles();

    // Locate or create mount target
    let target = document.getElementById('app-navbar') || document.querySelector('header');
    if (!target) {
        target = document.createElement('header');
        target.id = 'app-navbar';
        document.body.insertBefore(target, document.body.firstChild);
    }

    target.className = 'app-navbar';

    // Determine paths based on directory depth
    const path = window.location.pathname.replace(/\\/g, '/');
    const isSubdir = /\/(farmer|customer|wholesaler|driver|admin)\//.test(path);
    const basePath = isSubdir ? '../' : './';

    // Determine Role
    let role = options.role;
    if (!role) {
        if (path.includes('/farmer/')) role = 'farmer';
        else if (path.includes('/customer/')) role = 'customer';
        else if (path.includes('/wholesaler/')) role = 'wholesaler';
        else if (path.includes('/driver/')) role = 'driver';
        else if (path.includes('/admin/')) role = 'admin';
        else if (path.endsWith('login.html') || path.endsWith('login')) role = 'login';
        else if (path.endsWith('register.html') || path.endsWith('register')) role = 'register';
        else if (path.endsWith('seed.html') || path.endsWith('seed')) role = 'seed';
        else role = 'public';
    }

    let innerHtml = '';

    if (role === 'public') {
        target.classList.add('public-mode');
        innerHtml = `
            <div class="navbar-inner">
                <a href="${basePath}index.html" class="brand">
                    <div class="brand-icon">🌱</div>
                    <span>AgriTrace</span>
                </a>
                <nav class="nav-links-group">
                    <a href="#pipeline">Workflow</a>
                    <a href="#features">Features</a>
                    <a href="#portals">Role Portals</a>
                    <a href="${basePath}seed.html" style="color: #059669; font-weight: 700;">Demo Database</a>
                </nav>
                <div class="nav-right-group">
                    <a href="${basePath}login.html" class="btn btn-secondary btn-sm">Sign In</a>
                    <a href="${basePath}register.html" class="btn btn-sm">Join Network</a>
                </div>
            </div>
        `;
    } else if (role === 'login' || role === 'register' || role === 'seed') {
        target.classList.add('public-mode');
        const actionBtn = role === 'login' ? 
            `<a href="${basePath}register.html" class="btn btn-secondary btn-sm">Create Account</a>` :
            `<a href="${basePath}login.html" class="btn btn-secondary btn-sm">Sign In</a>`;

        innerHtml = `
            <div class="navbar-inner">
                <a href="${basePath}index.html" class="brand">
                    <div class="brand-icon">🌱</div>
                    <span>AgriTrace</span>
                </a>
                <nav class="nav-links-group">
                    <a href="${basePath}index.html">← Back to Overview</a>
                    <a href="${basePath}seed.html">Seed Database</a>
                </nav>
                <div class="nav-right-group">
                    ${actionBtn}
                </div>
            </div>
        `;
    } else {
        target.classList.remove('public-mode');
        const roleLabels = {
            farmer: { label: 'Farmer Hub', icon: '🌾', color: '#10b981', bg: 'rgba(16, 185, 129, 0.12)' },
            customer: { label: 'Customer Portal', icon: '🛒', color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.12)' },
            wholesaler: { label: 'Wholesaler Hub', icon: '🏬', color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.12)' },
            driver: { label: 'Driver Dispatch', icon: '🚚', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.12)' },
            admin: { label: 'System Admin', icon: '⚡', color: '#ef4444', bg: 'rgba(239, 68, 68, 0.12)' }
        };

        const currentRole = roleLabels[role] || { label: 'Portal', icon: '🌱', color: '#10b981', bg: 'rgba(16, 185, 129, 0.12)' };

        const cartHtml = role === 'customer' ? `
            <a href="cart.html" style="text-decoration: none;">
                <span id="cartCount" class="badge" style="background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; font-size: 0.85rem; padding: 0.4rem 0.9rem; cursor: pointer;">
                    🛒 0 items
                </span>
            </a>
        ` : '';

        innerHtml = `
            <div class="navbar-inner">
                <a href="dashboard.html" class="brand">
                    <div class="brand-icon">🌱</div>
                    <span>AgriTrace</span>
                    <span class="role-tag" style="color: ${currentRole.color}; background: ${currentRole.bg};">
                        ${currentRole.icon} ${currentRole.label}
                    </span>
                </a>
                <div class="nav-right-group user-info">
                    ${cartHtml}
                    <span id="userName">Loading...</span>
                    <button id="logoutBtn" class="btn btn-secondary">Sign Out</button>
                </div>
            </div>
        `;
    }

    target.innerHTML = innerHtml;
    return target;
}

// Auto-run if script is loaded
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => initNavbar());
    } else {
        initNavbar();
    }
}
