/**
 * Created by lite on 12/8/16.
 */

$(document).ready(function (){

    // Navbar collapsible dropdown button initialization for mobile
    $(".button-collapse").sideNav();

     $('ul.tabs').tabs();


});

function initTabs() {
    $('div.tab-content').css('display','none');

    $.each($('ul.tabs a'), function (key,value) {
       if($(value).hasClass('active')){
           target = $(value).attr('href');

           $(target).css('display','block');
       }
    });
}