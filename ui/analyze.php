<script>
	function run_tcgplayer_direct_analysis()
	{
		var buylist_id = $("#buylist").val();
		var command = 'c:/Python27/python.exe c:/workspace/python/analyzer/analyzer_tcg_player.py ' + buylist_id + " True";
		$.get('php_scripts/command_exec.php', {'command':command}, function(return_data)
		{
			var logs = "<div style='border-style:double;font-family: \"Courier New\", Courier, monospace;'>";
			for(ii = 0; ii < return_data.output.length; ++ii)
			{
				var line = return_data.output[ii];
				line = line.replace(/ /g, "&nbsp;");
				logs = logs + "<div>" + line + "</div>";
			}
			logs = logs + "</div>";
			
			$("#result").prepend(logs);

		}, "json");
	}
</script>
<div style="margin-bottom:20px;">
	<h1>Analyze</h1>
</div>

<div>
	<?php
		$sql = "select * from buy_list;";
		$result = $connection->query($sql);
		
		echo "<select name=\"buylist\" id=\"buylist\">";
		echo "<option value=\"\" selected disabled hidden>Select buylist</option>";
		while($row = $result->fetch())
		{
			echo "<option value=\"" . $row["id"] . "\">" . $row["name"] . "</option>";
		}
		echo "</select>";
	
		echo "<input type='submit' name='analyze' value='TCGPlayer Direct Analysis' onclick='run_tcgplayer_direct_analysis()'/>"
		//$command = escapeshellcmd('c:/Python27/python.exe c:/workspace/python/analyzer/analyzer_tcg_player.py 5');
		//$output = exec($command, $output);
		//echo $output;		
	?>
</div>

<div id="result">
</div>