/**
 * Created by Vaibhav on 18/9/16.
 */


$(document).ready(function(){
    
    var commit_log_open = false;                // flag varible for commit log
    $('ul.tabs').tabs();

    $('.commit-log').click(function (evt) {
        evt.preventDefault();

        if(!commit_log_open) {
            $('.commit-log-div').animate({width: "30%"});
            $('.project-directory').animate(({width: "70%"}));
            $('.commit-log-div').css('border-left','2px solid #888888');
            commit_log_open = true;
        }
        
        else {
            $('.commit-log-div').animate({width: "0"});
            $('.project-directory').animate(({width: "100%"}));
            $('.commit-log-div').css('border-left','none');
            commit_log_open = false;
        }
    });
});