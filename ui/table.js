// Update the text and onclick event of headers.
// container_id : id of the element containing the table.
// sort_column_id : current sorted column.
// dir : current sorted direction.
// type : type of the sorted column.
function update_header(container_id, sort_column_id, dir, type)
{
    containerElement = document.getElementById(container_id);
    tableElement = containerElement.firstChild;
    headerRowElement = tableElement.firstChild;

    for(let ii = 0; ii < headerRowElement.children.length; ++ii)
    {
        //get the raw name of the column
        headerCellElement = headerRowElement.children[ii];
        text = headerCellElement.textContent;

        const ASC_ARROW = "▲";
        const DESC_ARROW = "▼";

        text = text.replace(ASC_ARROW, "");
        text = text.replace(DESC_ARROW, "");

        let next_sorted_dir = "asc"
        if(ii == sort_column_id)
        {
            if(dir == "asc")
            {
                text = ASC_ARROW + " " + text;
                next_sorted_dir = "desc";
            }
            else
            {
                text = DESC_ARROW + " " + text;
                next_sorted_dir = "asc";
            }

            var currentCellSortedDir = next_sorted_dir
            headerCellElement.onclick = function () { sort_table(container_id, ii, currentCellSortedDir, type);};
        }

        headerCellElement.textContent = text;
    }
}

// Sort the table.
// container_id : element containing the table.
// column_id : id o the column to use to sort.
// sort_dir : direction to sort : asc or desc.
// type : type of data in the column.
function sort_table(container_id, column_id, sort_dir, type)
{
    var tableElement = $("#" + container_id).find("table")[0];

    //change the header sort function
    update_header(container_id, column_id, sort_dir, type);

    //simple bubble sort
    var rowArray = tableElement;
    var rowCount = rowArray.children.length;
    for(var ii = 1; ii < rowCount - 1; ++ii)
    {
        var rowElement = rowArray.children[ii];
        var value = rowElement.children[column_id].textContent;
        for(var jj = ii + 1; jj < rowCount; ++jj)
        {
            var anotherRowElement = rowArray.children[jj];
            var anotherValue = anotherRowElement.children[column_id].textContent;
            
            var value1;
            var value2;
            switch(type)
            {
                case "int":
                    if(isNaN(value))
                    {
                        value1 = value;
                        value2 = anotherValue;
                    }
                    else
                    {
                        value1 = parseInt(value);
                        value2 = parseInt(anotherValue);
                    }
                    break;

                case "float":
                    value1 = parseFloat(value);
                    value2 = parseFloat(anotherValue);
                    break;

                default:
                    value1 = value;
                    value2 = anotherValue;
                    break;
            }

            var switchRows = false;
            if (sort_dir == "asc" && value1 > value2)
            {
                switchRows = true;
            }
            else if(sort_dir == "desc" && value1 < value2)
            {
                switchRows = true;
            }

            if(switchRows)
            {
                //swap
                rowArray.insertBefore(anotherRowElement, rowElement);
                rowElement = anotherRowElement;
                value = anotherValue;
            }
        }
    }
}

// Display an array of data.
// container_id : id of the html element where to put the table.
// column_array : array of object describing the columns of the table. The variables are:
//      header_name : string to display in the header.
//      field_name : name of the field in the data.
//      type : type of data (int, float, string)
//                          special type : link to display an html link.
// data : array of rows containing the data to display in the table.
// field_row_id : field to use to set the id of each row in the table.
// sort_column_id : id of the column to use to sort the table.
// sort_dir : direction of the sort, asc or desc.
function display_table(container_id, column_array, data, field_row_id, sort_column_id, sort_dir)
{
    containerElement = document.getElementById(container_id);
    while (containerElement.firstChild) 
    {
        containerElement.removeChild(containerElement.firstChild);
    }

    tableElement = document.createElement("table");
    containerElement.appendChild(tableElement);

    // create headers
    headerRowElement = document.createElement("tr");
    tableElement.appendChild(headerRowElement);

    for(let ii = 0; ii < Object.keys(column_array).length; ++ii)
    {
        let column_data = column_array[ii];
        headerCellElement = document.createElement("th");

        headerCellElement.onclick = function () {sort_table(container_id, ii, "asc", column_data.type);};
        headerCellElement.textContent = column_data.header_name;
        headerRowElement.appendChild(headerCellElement);
    }

    for(ii=0; ii < Object.keys(data).length; ++ii)
    {
        var card = data[ii];
        
        rowElement = document.createElement("tr");
        rowElement.id = card[field_row_id];
        tableElement.appendChild(rowElement);
        for(var jj = 0; jj < Object.keys(column_array).length; ++jj)
        {
            var column_data = column_array[jj];

            cellElement = document.createElement("td");
            if(column_data.type == "link")
            {
                var htmlLink = document.createElement("a");
                htmlLink.href = card[column_data.field_name];
                htmlLink.textContent = "Link";
                htmlLink.target = "_blank";
                cellElement.appendChild(htmlLink);
            }
            else
            {
                cellElement.textContent = card[column_data.field_name];
            }
            
            rowElement.appendChild(cellElement);

            if(column_data.type == "float" || column_data.type == "int")
            {
                cellElement.style.textAlign = "right";
            }
        }
    }

    sort_table(container_id, sort_column_id, sort_dir, column_array[sort_column_id].type);
}

// Display the image of acard when mouse isover a row table.
// container_id : id of the html element containing the table.
// image_container_id : id of the img element to use to display the card.
// set_id : set_lang_id of the set displayed in the table.
function showCardImage(container_id, image_container_id, set_id)
{
	containerElement = document.getElementById(container_id);
	tableElement = containerElement.firstChild;

	rowCount = tableElement.childElementCount;

	let imageContainer = document.getElementById(image_container_id);//document.querySelector("#image");
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