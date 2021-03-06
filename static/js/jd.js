function jd_setck() {
    var datas = {
        jdCookies: $("#jdcookie").val(),
        remark: $("#remark").val(),
    };

    if (datas.jdCookies.indexOf("pt_key") === -1 && datas.jdCookies.indexOf("pt_pin") === -1) {
        $("#errorTips").text("您输入的cookies，不适用于本工具！请检查..").show();
        console.log("不包含子字符串")
    } else {
        console.log("包含子字符串")
    }

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

