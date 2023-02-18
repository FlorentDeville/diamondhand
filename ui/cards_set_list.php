<script>
$(document).ready(function()
{
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const set_id = urlParams.get('set_id');

	var sql = "select * from card where set_lang_id=" + set_id;
	$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
	{
		//show missing cards
		if(return_data.data.length>0)
		{
			$("#card_list_container").empty();
			
			var cards = return_data.data;
			var column_array = new Array();
			column_array.push({header_name:"O", field_name:"display_number", type:"int"});
			column_array.push({header_name:"N", field_name:"printed_number", type:"string"});
			column_array.push({header_name:"Name", field_name:"name", type:"string"});
			column_array.push({header_name:"Rarity", field_name:"rarity", type:"string"});
			column_array.push({header_name:"Var", field_name:"variation", type:"string"});
			column_array.push({header_name:"Links", field_name:"tcg_url", type:"link"});
			display_table("card_list_container", column_array, cards, "id", 0, "asc");

			containerElement = document.getElementById("card_list_container");
			tableElement = containerElement.firstChild;

			rowCount = tableElement.childElementCount;

			let imageContainer = document.querySelector("#image");
			const followMouse = (event) => 
			{
				imageContainer.style.left = event.x + "px";
				imageContainer.style.top = event.y + "px";
			}

			for(ii=1; ii < rowCount; ++ii)
			{
				rowElement = tableElement.childNodes[ii];
				let id = rowElement.id;
				
				let attached = false;
				rowElement.onpointerenter = function() 
				{
					if(!attached)
					{
						attached = true;
    					imageContainer.style.display = "block";
   						document.addEventListener("pointermove", followMouse);
						imageContainer.src = "./pics/sets/" + set_id + "/" + id + ".png";
					}
				};
				
				rowElement.onpointerleave = function()
				{
					attached = false;
  					imageContainer.style.display = "none";
  					document.removeEventListener("pointermove", followMouse);
				}
			}
		}
		else
		{
			$('#card_list_container').html('No records Found');
		}
	}, "json");
});
</script>
<div id="card_list_container"></div>
<img id="image" style="position:absolute; display:none; pointer-events:none; border:15px; border-color:transparent; border-style:double;"/>