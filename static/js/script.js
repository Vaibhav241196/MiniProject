/**
 * Created by lite on 12/8/16.
 */

$(document).ready(function (){

    // Navbar collapsible dropdown button initialization for mobile

    var target;

    initTabs();

    $('ul.tabs').tabs({
             onShow : function (currentTab) {
                 $(this).parent().parent().find('li a').removeClass('active');
                 $(this).addClass('active');

                 initTabs();
         }
     });




     // $('ul.tabs').tabs('select_tab', 'projects-shared');
     $(".button-collapse").sideNav();

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