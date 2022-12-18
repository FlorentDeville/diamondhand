<div id="stock_menu" style="margin:10 0 20 0;">
    <div style="display:inline;"> Stocks : </div>
</div>
<div id="content">
    <?php
        $page = "stock_overview.php";
        if(isset($_GET["stock_page"]))
        {
            $page = $_GET["stock_page"];
        }
        include("./" . $page);
    ?>
</div>

<script>
    function addMenuButton()
    {
        const urlParams = new URLSearchParams(window.location.search);
        const current_page = urlParams.get('stock_page');

        menuList = [];
        menuList.push({name:"Overview", link:"./index.php?page=stock_index.php&stock_page=stock_overview.php", id:"stock_overview.php"});
        menuList.push({name:"Table", link:"./index.php?page=stock_index.php&stock_page=stock_overview_table.php", id:"stock_overview_table.php"});
        menuList.push({name:"All", link:"./index.php?page=stock_index.php&stock_page=stock_view.php", id:"stock_view.php"});
        menuList.push({name:"Sets", link:"./index.php?page=stock_index.php&stock_page=stock_view_set.php", id:"stock_view_set.php"});
        menuList.push({name:"Add single cards", link:"./index.php?page=stock_index.php&stock_page=stock_add_card.php", id:"stock_add_card.php"});
        menuList.push({name:"Add card lists", link:"./index.php?page=stock_index.php&stock_page=stock_add_card_list.php", id:"stock_add_card_list.php"});

        var menu = document.getElementById("stock_menu");
        for(var ii = 0; ii < menuList.length; ++ii)
        {
            item = menuList[ii];
            var gameButton = document.createElement("a");
            gameButton.href = item.link;
            if(item.id == current_page)
                gameButton.classList.add("selectedStockMenuButton");
            else
                gameButton.classList.add("stockMenuButton");

            gameButton.style.padding="0px 2px 0px 2px";

            var buttonContent = document.createElement("div");
            buttonContent.textContent=item.name;
            buttonContent.classList.add("stockMenuButton");
            gameButton.appendChild(buttonContent);

            menu.appendChild(gameButton);
        }
    }

    addMenuButton();
</script>