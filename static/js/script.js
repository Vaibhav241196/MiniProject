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
                $("#member-list").append("<li value=" + res.id + " class='member'>"+ userName + "</li>");

            else
                alert("No such user found");
        }).
            fail(function (err) {
                console.log(err);
        });

    });

    $("form#new_project").submit(function(evt){

        evt.preventDefault();
        console.log('Test');
        var projectData = {};

        projectData.projectName = $("input#project-name").val();
        projectData.projectDescription = $("input#project-description").val();
        projectData.projectMembers = [];

        var members = $("#member-list li");

        console.log(members.length);

        // for (i in members) {
        //     console.log($(members[i]).attr('value'));
        //     // data.projectMembers.push($(members[i]).attr('value'));
        // }

        console.log(members);

        $.each($("#member-list li"),function (index,value){
            projectData.projectMembers.push($(value).attr('value'));
        });

        console.log(projectData);
        $.ajax({
            url: '/createProject',
            method: 'POST',
            data : JSON.stringify(projectData),
            contentType: 'application/json',
            dataType : 'html',
        }).
            done(function(res) {
                document.write(res);
        }).
            fail(function (err) {
                console.log(err);
        });
    });
});
