// Set the onclick event of a header
// container_id : element containing the table.
// column_id : id of the column header to change.
// dir : direction of the sort.
// type : type of data in the column.
function make_header_onclick(container_id, column_id, dir, type)
{
    var tableElement = $("#" + container_id).find("table")[0];
    var tr = tableElement.firstChild;//.children[0];
    var th = tr.children[column_id];
    th.onclick = function() {sort_table(container_id, column_id, dir, type);};
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
    make_header_onclick(container_id, column_id, sort_dir == "asc" ? "desc" : "asc", type);

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
                    value1 = parseInt(value);
                    value2 = parseInt(anotherValue);
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
//      type : type of data (int, string)
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

    // display headers
    headerRowElement = document.createElement("tr");
    tableElement.appendChild(headerRowElement);

    for(var ii = 0; ii < Object.keys(column_array).length; ++ii)
    {
        var column_data = column_array[ii];
        var ASC_ARROW = "▲";
        var DESC_ARROW = "▼";

        var arrow = "";
        var dir = "asc";
        if (ii == sort_column_id)
        {
            if(dir == "desc")
            {
                //arrow = DESC_ARROW + " ";
                dir = "asc";
            }
            else
            {
                //arrow = ASC_ARROW + " ";
                dir = "desc";
            }
        }

        headerCellElement = document.createElement("th");
        var col_id = ii;
        headerCellElement.onclick = function () { sort_table(container_id, col_id, dir, column_data.type);};
        headerCellElement.textContent = arrow + column_data.header_name;
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
            cellElement.textContent = card[column_data.field_name];
            rowElement.appendChild(cellElement);
        }
    }

    sort_table(container_id, sort_column_id, sort_dir, column_array[sort_column_id].type);
}