<?php
	//find the last price per sealed products
	$sql = "select max(id) as id from sealed_products_price_history group by sealed_product_id";
	$query = $connection->query($sql);
	$last_ids = $query->fetchAll();
	//echo json_encode($last_ids);
	
	$in_ids = "";
	foreach ($last_ids as $row)
	{
		if($in_ids != "")
			$in_ids = $in_ids . ", ";
		$in_ids = $in_ids . "\"" . $row["id"] . "\"";
	}
	
	$sql = "select s.id, s.name, o.acq_date, o.acq_price, p.price, p.date 
			from sealed_products as s inner join sealed_products_price_history as p on s.id = p.sealed_product_id
			inner join owned_sealed_products as o on s.id = o.sealed_product_id 
			where p.id in (" . $in_ids . ");";
	//echo $sql;
	$query = $connection->query($sql);
	$sealed_products = $query->fetchAll();
	
	//Tab Header
	echo "<table>";
	echo "<tr><th>Name</th><th>Acq Price</th><th>Acq Date</th><th>Last Sold Price</th><th>Delta</th>";

	foreach ($sealed_products as $sealed)
	{
		$name = $sealed["name"];
		$acq_price = $sealed["acq_price"];
		$acq_date = $sealed["acq_date"];
		$last_sold_price = $sealed["price"];
		$dt = ($last_sold_price - $acq_price) / $acq_price;
		$link = "index.php?page=sealed_history.php&sealed_id=" . $sealed["id"];
		
		$arrow_class = "up green";
		if($dt < 0)
		$arrow_class = "down red";
		
		$arrow_div = "<span class=\"" . $arrow_class . "\"></span>";
		$percent = "<span>" . $dt . "%</span>";
		echo "<tr><td><a class=\"standard_link\" href=\"" . $link . "\">" . $name . "<a/></td><td>" . $acq_price . "</td><td>" . $acq_date . "</td><td>" . $last_sold_price . "</td><td>" . $arrow_div . $percent . "</td></tr>";
	}
	echo "</table>";
	
?>
			