$(document).ready(function(){

    $("#T1").trigger('click');
    $('#sideBarButton').click();

});

function roomTableEntry(frm) {

    console.log("on click on placeorder on modal");
    const formData = new FormData(frm); 
    let flag = 1;
    let data = ["rishi"];
    //   let i = 0;
    //   let names = ['csrfid','first','last','email','comment'];
    for (var value of formData.values()) {
        console.log(value);
        if (value == "") {  
            flag = 0;
        }
        data.push(value);
    }
    console.log(data);
    let room_name = data[2];
    let table_nos = data[3];
    // let Members = data[4]
    let sendData = {
        room_name: room_name,
        table_nos: table_nos,
    };
    console.log(sendData);
    if (flag != 0) {
        var csrftoken = $.cookie("csrftoken");
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            }
        });

        $.ajax
            ({
            type: "POST",
            url: "",
            data: sendData,
            success: function (data) {
                console.log("Success");
                $("input[name='room_name']").val('');
                $("input[name='room_table']").val('');
                $("#T1").trigger('click');
                $("#displayLayout" ).load(window.location.href + " #displayLayout" );
                $("#roomTable" ).load(window.location.href + " #roomTable" );                
                return 1;
            }
        });
    }
};