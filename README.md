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
- SQLite

---

## Installation & Setup

Follow these steps to run the project:

# Clone the repository
Your API will be available at:  
`http://127.0.0.1:8000/`

---

## 📡 List of API Endpoints

# Authentication
---------------------------------------------------------------------
| Method | Endpoint         | Description                            |
|--------|------------------|----------------------------------------|
| POST   | `/api/register/` | Register a user (owner/staff/customer) |
| POST   | `/api/login/`    | Login and get JWT access token         |
----------------------------------------------------------------------

---

### Products (Tenant-Specific)
-----------------------------------------------------------------------
| Method | Endpoint              | Description                        |
|--------|-----------------------|------------------------------------|
| GET    | `/api/products/`      | List products for logged-in tenant |
| POST   | `/api/products/`      | Create product                     |
| PUT    | `/api/products/<id>/` | Update product                     |
| DELETE | `/api/products/<id>/` | Delete product                     |
-----------------------------------------------------------------------

---

### `Orders (Tenant-Specific)
--------------------------------------------------------
| Method | Endpoint       | Description                |
|--------|----------------|----------------------------|
| POST   | `/api/orders/` | Place order                |
| GET    | `/api/orders/` | List orders for the tenant |
--------------------------------------------------------

---

## Multi-Tenancy Implementation (Short Note)

- Each vendor (tenant) is stored in a `Tenant` model with details like store name, contact, and domain.
- Every user belongs to exactly one tenant.
- JWT token includes `tenant_id`, so every request automatically knows which tenant is making the request.
- A custom middleware attaches `request.tenant` to each request.
- All queries are filtered by tenant:
Model.objects.filter(tenant=request.tenant)

- Vendors cannot see or modify each other’s data.

---

##  Role-Based Access (Short Note)

- Each user has a role: `owner`, `staff`, or `customer`.
- Roles are stored in the database and included in the JWT token.
- Custom DRF permissions restrict access:
- **Owner** → full access (products, orders, staff management)
- **Staff** → can manage assigned products & orders only
- **Customer** → can view products and place orders
- Unauthorized users receive `403 Forbidden`.

---
