CREATE TABLE IF NOT EXISTS brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    parent_category_id INT REFERENCES category(category_id),
    level SMALLINT NOT NULL CHECK (level IN (1, 2)),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS seller (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(150) NOT NULL,
    join_date DATE NOT NULL,
    seller_type VARCHAR(50) NOT NULL CHECK (seller_type IN ('Official', 'Marketplace')),
    rating DECIMAL(2,1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
    country VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS customer (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female')),
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category_id INT NOT NULL REFERENCES category(category_id),
    brand_id INT NOT NULL REFERENCES brand(brand_id),
    seller_id INT NOT NULL REFERENCES seller(seller_id),
    price DECIMAL(12,2) NOT NULL CHECK (price > 0),
    stock_qty INT NOT NULL CHECK (stock_qty >= 0),
    rating DECIMAL(2,1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
    created_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customer(customer_id),
    order_date TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (
        status IN ('PLACED', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED')
    ),
    total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),
    created_at TIMESTAMP NOT NULL CHECK (created_at >= order_date)
);

CREATE TABLE IF NOT EXISTS order_item (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id),
    product_id INT NOT NULL REFERENCES product(product_id),
    order_date TIMESTAMP NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price > 0),
    subtotal DECIMAL(12,2) NOT NULL CHECK (subtotal = quantity * unit_price),
    created_at TIMESTAMP NOT NULL CHECK (created_at >= order_date)
);

CREATE TABLE IF NOT EXISTS promotion (
    promotion_id SERIAL PRIMARY KEY,
    promotion_name VARCHAR(100) NOT NULL,
    promotion_type VARCHAR(50) NOT NULL CHECK (
        promotion_type IN ('product', 'category', 'seller', 'flash_sale')
    ),
    discount_type VARCHAR(20) NOT NULL CHECK (
        discount_type IN ('percentage', 'fixed_amount')
    ),
    discount_value NUMERIC(10,2) NOT NULL CHECK (
        discount_value > 0
        AND (discount_type = 'fixed_amount' OR discount_value <= 100)
    ),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    CHECK (start_date >= created_at::date),
    CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS promotion_product (
    promo_product_id SERIAL PRIMARY KEY,
    promotion_id INT NOT NULL REFERENCES promotion(promotion_id),
    product_id INT NOT NULL REFERENCES product(product_id),
    created_at TIMESTAMP NOT NULL,
    UNIQUE (promotion_id, product_id)
);
