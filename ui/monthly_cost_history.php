<?php
	$sql = "SELECT sum(acq_price) as price, DATE_FORMAT(acq_date, '%m/%y') as date, month(acq_date) as month, year(acq_date) as year FROM `owned_card` group by date order by year asc, month asc";
	$query = $connection->query($sql);
	$rows = $query->fetchAll();
	echo "<div id=\"data\" hidden>";
	echo json_encode($rows);
	echo "</div>";
?>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(drawChart);
  
	function drawChart() 
	{
		var dataElement = document.getElementById('data');
		var text = dataElement.textContent;
		var json_data = JSON.parse(text);
		var title = json_data[0]["name"];
		
		var data_array = [['Date', 'Price']];
		for(var ii = 0; ii < json_data.length; ++ii)
		{
			var date = json_data[ii]["date"];
			var price = parseFloat(json_data[ii]["price"]);
			data_array.push([date, price]);
		}
		
		var data = google.visualization.arrayToDataTable(data_array);
		var options = 
		{
			title: title,
			legend: 
			{ 
				position: 'bottom', 
				textStyle:
				{
					color:'white'
				}
			},
			backgroundColor:
			{
				fill: 'black',
				stroke: 'white',
				strokeWidth: 1
			},
			hAxis: 
			{
				textStyle:{color: 'white'}
			},
			vAxis: 
			{
				textStyle:{color: 'white'}
			}
		};

		var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

		chart.draw(data, options);
	}
</script>
<div id="curve_chart" style="width: 900px; height: 500px"></div>

		