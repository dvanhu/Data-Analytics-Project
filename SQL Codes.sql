-- Top 10 highest revenue-generating products overall
SELECT TOP 10 
    product_id,
    SUM(sale_price) AS total_sales
FROM df_orders
GROUP BY product_id
ORDER BY total_sales DESC;


-- Top 5 best-selling products by sales in each region
WITH regional_sales AS (
    SELECT 
        region,
        product_id,
        SUM(sale_price) AS total_sales
    FROM df_orders
    GROUP BY region, product_id
)
SELECT *
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY total_sales DESC) AS rank
    FROM regional_sales
) ranked_sales
WHERE rank <= 5;


-- Month-over-month sales comparison for 2022 vs 2023
WITH monthly_sales AS (
    SELECT 
        YEAR(order_date) AS order_year,
        MONTH(order_date) AS order_month,
        SUM(sale_price) AS total_sales
    FROM df_orders
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT 
    order_month,
    SUM(CASE WHEN order_year = 2022 THEN total_sales ELSE 0 END) AS sales_2022,
    SUM(CASE WHEN order_year = 2023 THEN total_sales ELSE 0 END) AS sales_2023
FROM monthly_sales
GROUP BY order_month
ORDER BY order_month;


-- Find the month with the highest sales for each category
WITH category_monthly_sales AS (
    SELECT 
        category,
        FORMAT(order_date, 'yyyyMM') AS year_month,
        SUM(sale_price) AS total_sales
    FROM df_orders
    GROUP BY category, FORMAT(order_date, 'yyyyMM')
)
SELECT *
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_sales DESC) AS rank
    FROM category_monthly_sales
) ranked_category_sales
WHERE rank = 1;


-- Sub-category with highest sales growth (2023 vs 2022)
WITH yearly_subcategory_sales AS (
    SELECT 
        sub_category,
        YEAR(order_date) AS order_year,
        SUM(sale_price) AS total_sales
    FROM df_orders
    GROUP BY sub_category, YEAR(order_date)
),
sales_comparison AS (
    SELECT 
        sub_category,
        SUM(CASE WHEN order_year = 2022 THEN total_sales ELSE 0 END) AS sales_2022,
        SUM(CASE WHEN order_year = 2023 THEN total_sales ELSE 0 END) AS sales_2023
    FROM yearly_subcategory_sales
    GROUP BY sub_category
)
SELECT TOP 1 
    sub_category,
    sales_2022,
    sales_2023,
    (sales_2023 - sales_2022) AS growth
FROM sales_comparison
ORDER BY growth DESC;
