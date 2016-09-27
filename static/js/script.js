/**
 * Created by lite on 12/8/16.
 */

$(document).ready(function (){

    // Navbar collapsible dropdown button initialization for mobile
    $(".button-collapse").sideNav();
    $('ul.tabs').tabs();


    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();

    // For select buttons
    $('select').material_select();

    $("a#members-form-submit").click(function(evt){

        console.log('Test');
        evt.preventDefault();
        var userName = $("input#member-name").val();

        $.ajax({
            url: '/checkMembers',
            method: 'POST',
            data : { member_name: userName },
            dataType : 'json',
        }).
            done(function(res) {

            if(res.status === true)
                $("#member-list").append("<li class='member'>"+ userName + "</li>");

            else
                alert("No such user found");
        }).
            fail(function (err) {
                console.log(err);
        });

    });

});
