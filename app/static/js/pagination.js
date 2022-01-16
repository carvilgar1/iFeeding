function addPageNumToFormAndSend(pageNum){
    var input = document.createElement("input");

    input.setAttribute("type", "hidden");

    input.setAttribute("name", "page_num");

    input.setAttribute("value", pageNum);

    //append to form element that you want .
    document.getElementById("extended_search_form").appendChild(input);
    document.getElementById("extended_search_form").submit();
}