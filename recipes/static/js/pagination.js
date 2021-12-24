var total_len = document.getElementById("result_len").innerHTML;
var page_num = document.getElementById("page_num");
var page_len = document.getElementById("page_len"); 

if (page_num.value < 1){
    page_num.value = 1;
}

if (page_len.value < 1){
    page_len.value = 15;
}

var total_pages = Math.ceil(total_len/page_len.value)

if(page_num.value > total_pages){
    page_num.value = total_pages;
}