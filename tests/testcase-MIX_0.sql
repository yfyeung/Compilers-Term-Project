SELECT DISTINCT cust_city, SUM (opening_amt) FROM customer GROUP BY cust_city HAVING MAX(customer.cust_city)<=10
