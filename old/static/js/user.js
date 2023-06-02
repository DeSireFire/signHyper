// if(document.documentElement.contains(node)) { alert("存在"); }
// alert(window.location.href);

window.onhashchange=function(event){
  console.log(event);
}
//或者
window.addEventListener('hashchange',function(event){
   console.log(event);
})

if (getCookie("jd-user")) {
    change_name()
}

function change_name(){
    var name = getCookie("jd-user");
    // alert(name);
    $("#jd-user").text("欢迎您访问, "+name);
}

// 获取指定名称的cookie
function getCookie(name){
    var strcookie = document.cookie;//获取cookie字符串
    var arrcookie = strcookie.split("; ");//分割
    console.log("获取到cookie"+strcookie)
    //遍历匹配
    for ( var i = 0; i < arrcookie.length; i++) {
        var arr = arrcookie[i].split("=");
        if (arr[0] == name){
            return arr[1];
        }
    }
    return "网络旅行者";
}