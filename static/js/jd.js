function login() {
    var datas = {
        jdCookies: $("#jdcookie").val(),
        remark: $("#remark").val(),
    };
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/api/jdApp/setck",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(datas),
		// headers:{"Content-Type":"application/json","accept":"application/json"},
        success: function (data) {
            if (data.status == "0") {
                $("#errorTips").text(data.errMsg).show();
                $("#loginBtn").text("提交托管");
            } else {
                window.location.href = "/user";
            }
        }
    });
}