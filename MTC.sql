-- генерация случайных данных (отдельно создает индекс на таблице, перед апуском возможно нужно закомментировать)

DO $$
DECLARE 
	order_cnt INTEGER := floor(random()*100000);
	o_id INTEGER := 0;
	r_date DATE;
	order_amount INTEGER;
	items_cnt INTEGER;
	items VARCHAR(15)[15] := ARRAY['товар1','товар2','товар3','товар4','товар5','товар6','товар7','товар8','товар9','товар10','товар11','товар12','товар13','товар14','товар15'];
	
BEGIN

--  	DROP TABLE IF EXISTS cb_order_item ;
--  	DROP TABLE IF EXISTS cb_order;


	CREATE TABLE IF NOT EXISTS cb_order (
	  order_id serial UNIQUE PRIMARY KEY,
	  name VARCHAR(20), 
	  amount INTEGER NOT NULL,
	  request_date DATE NOT NULL
	  );

	CREATE TABLE IF NOT EXISTS cb_order_item (
	  id_item serial UNIQUE PRIMARY KEY,
	  order_id INTEGER REFERENCES cb_order (order_id) ON DELETE CASCADE ON UPDATE CASCADE, 
	  item_name VARCHAR(20),
	  item_quantity integer CHECK (item_quantity > 0), 
	  item_amount integer CHECK (item_amount > 0)
	);
	
	CREATE INDEX IF NOT EXISTS item_amount_idx ON cb_order_item (item_amount);
	
	--RAISE NOTICE 'value %', order_cnt;
	WHILE order_cnt > 0 LOOP
		SELECT floor(random()*10000) INTO order_amount;
		SELECT floor(random()*20 + 1) INTO items_cnt;
		SELECT timestamp '2022-01-01 00:00:00' + random() * (timestamp '2022-02-15 00:00:00' - timestamp '2022-01-01 00:00:00')  INTO r_date;
		INSERT INTO cb_order(name, amount, request_date) VALUES ('Покупка №' || trim(both from to_char(o_id, '99999999')),order_amount,r_date);
		SELECT currval(pg_get_serial_sequence('cb_order','order_id')) INTO o_id;
		
		WHILE items_cnt > 0 LOOP
			INSERT INTO cb_order_item(order_id, item_name, item_quantity, item_amount) VALUES (o_id, items[floor(random()*15)], floor(random()*20+1), floor(random()*2000+100));
			items_cnt := items_cnt - 1;
		END LOOP;
		
		order_cnt := order_cnt - 1;
	END LOOP;
	
	
END $$;


-- задача 1
SELECT *
  	FROM cb_order o
  	WHERE  o.request_date BETWEEN CURRENT_DATE - INTERVAL '7 day' AND CURRENT_DATE;


-- задача 2 (если правильно понял, что >3 относится именно к количеству позиций в заказе у каждой из которых есть item_quantity , а не к item_quantity )
SELECT *
  	FROM cb_order o
   	INNER JOIN cb_order_item oi ON o.order_id = oi. order_id
  	WHERE o.order_id IN (
 		SELECT oid 
 			FROM (
    				SELECT order_id AS oid, count(*) 
    					FROM cb_order_item
    					WHERE order_id IN (
    							SELECT DISTINCT cb.order_id 
    								FROM cb_order_item cb
    								WHERE cb.item_amount > 1000
    						) 
    					GROUP BY 1 
    					HAVING count(*) > 3 
 					) foo
 	)
	ORDER BY 1;


