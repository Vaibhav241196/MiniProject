/**
 * Created by lite on 12/8/16.
 */

$(document).ready(function (){


    var clickedFolder = null;

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
            url: '/check_members',
            method: 'POST',
            data : { member_name: userName },
            dataType : 'json',
        }).
            done(function(res) {

            if(res.status === 0) {
                $("#member-list").append("<li value=" + res.id + " class='member'>" + userName + "</li>");
                $("input#member-name").val("");
            }

            else if (res.status === 1)
                alert(res['message']);

            else if(res.status === 2) {
                alert(res['message'])
            }
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
            url: '/create_project',
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

    /*================ Adds single click functionality for project folder ======================= */

    var folders = $(".single-project-listing");

    folders.click(function(){

        console.log("In single project listing");
        if (clickedFolder)
                clickedFolder.css("background-color","white");

            $(this).css("background-color","#BBDEFB");
            $("#nav-bar-right").css("display","block");
            clickedFolder = $(this);
            $("#download-project-id").val(clickedFolder.attr('id'));
    });

    $(".content-main").click(function(evt) {

        if(! ( $(evt.target).hasClass('single-project-listing') || $(evt.target).hasClass('fa') ) ){
            if (clickedFolder)
                clickedFolder.css("background-color", "white");

            $("#nav-bar-right").css("display", "none");
        }
    });
    $("#searchForm").submit(function (evt) {
       // $('#submitButton').click(function(evt) {
            evt.preventDefault();
            var domainSearch = [];
            domainSearch = $('#multiselection').val();
            var chipSearch = [];
            var str = $('#search').val();
            chipSearch = str.split(" ");

            var data = {};
            data = {"domainSearch": domainSearch, "chipSearch": chipSearch};
           // alert(data.domainSearch)
            //alert(multiselect);
            alert(chipSearch[2])
            $.ajax({
                url: '/search',
                method: 'POST' ,
                data: data,
                dataType: 'json'

            }).done(function (data) {

                for(var i =0;i < data.array.length-1;i++)
                {
                    console.log(i);
                    $('#foundResults').append('<div class = "col l2 m4 s6 offset-m1 center-align"><div class="single-project-listing center-align" id='+data.array[i]._id+'><a href="#"><i class="fa fa-folder" aria-hidden="true" id="projFolder"></i></a> </div><p>'+data.array[i].projName+'</p></div>')

                }
               // data.array[i].projectName

              //  '<div class="" id=' + data.array[i]._id + ''


            }).fail(function (err) {
                console.log(err);

            });
        });
    //
    // <div class="row">
    //
    //                         {% for i in aggregate %}
    //                             <div class = "col l12 m12 s12">
    //                             <h4 style="font-family: EB garamond, sans-serif; text-decoration: underline; text-transform: capitalize">{{i['_id']}}</h4>
    //                             </div>
    //
    //                             {% for j in range((i['projectName']|length)) %}
    //
    //                             <div class="col l2 m4 s6 offset-m1 center-align">
    //                                 <div class="single-project-listing center-align" id="{{ i['projectId'][j] }}">
    //                                     <a href="#"><i class="fa fa-folder" aria-hidden="true" id="projFolder"></i></a>
    //                                 </div>
    //                                 <p>{{i['projectName'][j]}}</p>
    //                                 </div>
    //                              {% endfor%}
    //                         {% endfor %}
    // {#                    {% endif %}#}
    //                     </div>/
    //

    $("#rename-project-form").submit(function(evt){
        evt.preventDefault();

        var data = {};
        data.proj_id = clickedFolder.attr('id');
        data.new_name = $("#new_project_name").val();

        $.ajax({
            url: '/rename',
            method: 'POST',
            data: data,
            dataType: 'json'
        }).
            done(function(data) {
                clickedFolder.parent().find("p").text(data.new_name);
        }).
            fail(function (err){
                console.log(err);
        });

    });

    $("#delete-project").click(function(evt){

        console.log("In delete");
        var data = {};
        data.proj_id = clickedFolder.attr('id');

        $.ajax({
            url: '/delete',
            method: 'POST',
            data: data,
            dataType: 'json'
        }).
            done(function(data){
                if(data.status == 0) {
                    clickedFolder.parent().remove();
                    alert(data.message)
                }

                else if (data.status == 1) {
                    alert(data.message)
                }
        }).
            fail(function(err){
            console.log(err)
        });
    });

    $("#download-project").click(function (evt){
        $("form#download-project-form").submit();
    });


    folders.dblclick(function(){
        window.location.assign("project_dashboard");
    });
});

$(document).ready(function () {
    $('select').material_select();
    $('select').change(function(){
        var newValuesArr = [],
            select = $(this),
            ul = select.prev();
        ul.children('li').toArray().forEach(function (li, i) {
            if ($(li).hasClass('active')) {
                newValuesArr.push(select.children('option').toArray()[i].value);
            }
        });
        select.val(newValuesArr);
           console.log(newValuesArr);
    });

});