<script>
	function run_tcgplayer_direct_analysis()
	{
		$("#loading_icon").css("visibility", "visible");
		var buylist_ids = $("#buylist").val();
		var buylist_arg = "";
		for(ii = 0; ii < buylist_ids.length; ++ii)
		{
			buylist_arg = buylist_arg + " -buylist-id " + buylist_ids[ii]
		}

		var command = 'c:/Python27/python.exe c:/workspace/python/analyzer/analyzer_tcg_player.py ' + buylist_arg + " -direct";
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
			$("#loading_icon").css("visibility", "hidden");
		}, "json");
	}
	
	function run_tcgplayer_analysis()
	{
		$("#loading_icon").css("visibility", "visible");
		var buylist_ids = $("#buylist").val();
		var buylist_arg = "";
		for(ii = 0; ii < buylist_ids.length; ++ii)
		{
			buylist_arg = buylist_arg + " -buylist-id " + buylist_ids[ii]
		}
		
		var command = 'c:/Python27/python.exe c:/workspace/python/analyzer/analyzer_tcg_player.py ' + buylist_arg;
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
			$("#loading_icon").css("visibility", "hidden");
		}, "json");
	}

</script>
<style>
.loader 
{
  border: 16px solid #f3f3f3; /* Light grey */
  border-top: 16px solid #818181; /* Blue */
  border-bottom: 16px solid #818181; /* Blue */
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
}

@keyframes spin 
{
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
<div style="margin-bottom:20px;">
	<h1>Analyze</h1>
</div>

<div>
	<?php
		$sql = "select * from buy_list;";
		$result = $connection->query($sql);
		
		echo "<select name=\"buylist\" id=\"buylist\" multiple size=\"10\">";
		echo "<option value=\"\" selected disabled hidden>Select buylist</option>";
		while($row = $result->fetch())
		{
			echo "<option value=\"" . $row["id"] . "\">" . $row["name"] . "</option>";
		}
		echo "</select>";
		
		echo "<div style=\"display:inline-block;\">";
		echo "<div><input type='submit' name='analyze' value='TCGPlayer Direct Analysis' onclick='run_tcgplayer_direct_analysis()'/></div>";
		echo "<div><input type='submit' name='analyze' value='TCGPlayer Analysis' onclick='run_tcgplayer_analysis()'/></div>";
		echo "</div>";
	?>
	<div id="loading_icon" style="width:25;height:25;display:inline-block;visibility:hidden;" class="loader"></div>
</div>
<div id="result">
</div>
