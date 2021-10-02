function get_array_header(field, dir, title, show_arrow, set_id)
{
    var reverse_dir = "desc";
    var arrow = "▲";
    if(dir == "desc")
    {
        arrow = " ▼";
        reverse_dir = "asc";
    }
    
    if(!show_arrow)
        arrow = "";

    var content = "<span onclick=\"show_set(" + set_id + ",'" + field + "','" + reverse_dir + "')\">" + title + arrow + "</span>";
    return content;
}

//Display an array of data
// container_id : id of the html element where to put the table.
// column_array : array of object describing the columns of the table. The variables are:
//      header_name : string to display in the header.
//      field_name : name of the field in the data.
// data : array of rows containing the data to display in the table.
// field_row_id : field to use to set the id of each row in the table.
function display_table(container_id, column_array, data, field_row_id)
{
    var content = "<table>";

    content += "<tr>";
    for(var ii = 0; ii < Object.keys(column_array).length; ++ii)
    {
        var column_data = column_array[ii];
        //var header = get_array_header(header_data["field"], sort_dir, header_data["title"], header_data["field"] == sort_field, set_id);
        var header = column_data.header_name;
        content += "<th>" + header + "</th>";
    }

    for(ii=0; ii < Object.keys(data).length; ++ii)
    {
        var card = data[ii];
        
        content += "<tr id='" + card[field_row_id] + "'>";
        for(var jj = 0; jj < Object.keys(column_array).length; ++jj)
        {
            var column_data = column_array[jj];
            content += "<td>" + card[column_data.field_name] + "</td>";
        }

        content += "</tr>";
    }
    content += "</table>";

    $("#" + container_id).empty();
    $("#" + container_id).prepend(content);
}