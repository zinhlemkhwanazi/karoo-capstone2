
-- schema.sql
-- Database schema for Karoo Organics (SQL Server 2022)

IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name = N'KarooOrganics')
BEGIN
    CREATE DATABASE KarooOrganics;
END;
GO

USE KarooOrganics;
GO

-- =============================
-- Core Tables
-- =============================

-- Suppliers
CREATE TABLE dbo.Suppliers (
    supplier_id INT NOT NULL PRIMARY KEY,               
    farm_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    contact_email VARCHAR(100) UNIQUE
);
GO

-- Orders
CREATE TABLE dbo.Orders (
    order_id INT NOT NULL PRIMARY KEY,                  
    supplier_id INT NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    total_price AS (quantity * unit_price) PERSISTED,   
    CONSTRAINT FK_Orders_Suppliers
        FOREIGN KEY (supplier_id) REFERENCES dbo.Suppliers(supplier_id)
);
GO

-- =============================
-- New Tables for Q4 Report
-- =============================

-- Sales targets per region and quarter
CREATE TABLE dbo.Sales_Targets (
    region VARCHAR(50) NOT NULL,
    quarter VARCHAR(6) NOT NULL,                        -- e.g., 'Q4-2025'
    target_amount DECIMAL(12,2) NOT NULL CHECK (target_amount > 0),
    CONSTRAINT PK_Sales_Targets PRIMARY KEY (region, quarter)
);
GO

-- Certifications held by suppliers
CREATE TABLE dbo.Certifications (
    certification_id INT IDENTITY(1,1) PRIMARY KEY,
    supplier_id INT NOT NULL,
    certification_name VARCHAR(100) NOT NULL,
    issued_by VARCHAR(100),
    issue_date DATE,
    CONSTRAINT UQ_Certifications UNIQUE (supplier_id, certification_name),
    CONSTRAINT FK_Certifications_Suppliers
        FOREIGN KEY (supplier_id) REFERENCES dbo.Suppliers(supplier_id)
);
GO

-- Harvest logging for operational tracking
CREATE TABLE dbo.Harvest_Log (
    harvest_id INT IDENTITY(1,1) PRIMARY KEY,
    supplier_id INT NOT NULL,
    harvest_date DATE NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    quantity_kg DECIMAL(10,2) NOT NULL CHECK (quantity_kg > 0),
    CONSTRAINT FK_Harvest_Suppliers
        FOREIGN KEY (supplier_id) REFERENCES dbo.Suppliers(supplier_id)
);
GO

-- =============================
-- Indexes for Performance
-- =============================

CREATE INDEX idx_orders_supplier ON dbo.Orders(supplier_id);
CREATE INDEX idx_orders_date ON dbo.Orders(order_date);
CREATE INDEX idx_harvest_supplier ON dbo.Harvest_Log(supplier_id);
GO
