# Multi-Tenant E-Commerce Backend (Django + DRF + JWT)

A backend system that supports multiple vendors (tenants) on a shared platform.  
Each vendor can manage their own products, orders, and customers independently.


# Multi-Tenancy
- Each vendor has isolated:
  - Products  
  - Orders  
  - Customers  
- JWT contains `tenant_id`
- Middleware automatically attaches tenant to each request
- Vendor cannot access another vendor’s data

# Role-Based Access (RBAC)
- **Owner** → Full access (products, orders, users)
- **Staff** → Can manage assigned products & orders
- **Customer** → Can view products & place orders

# SuperUser
- Username-> admin
- Password-> admin

# Authentication
- JWT-based login & registration
- Token includes: `tenant_id`, `role`, `user_id`

---

# Tech Stack

- Python  
- Django  
- Django REST Framework  
- JWT Authentication  
- SQLite/PostgreSQL  

---

## 📦 Installation & Setup

Follow these steps to run the project:

# Clone the repository
