function get_sort_arrow(field, dir, title, show_arrow)
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

	var content = "<span onclick=\"show_set('" + field + "','" + reverse_dir + "')\">" + title + arrow + "</span>";
	return content;
}
