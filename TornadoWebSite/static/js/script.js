//$(document).ready(function(){
//    alert("good");
//    $("#login").click(function(){
//        var user=$("#username").val();
//        var pwd=$("#password").val();
//        alert("username:"+user)
//    });
//})

$(document).ready(function(){
//    alert("good");
    $("#login").click(function(){
        var user=$("#username").val();
        var pwd=$("#password").val();
        var pd={"username":user,password:pwd};
        $.ajax({
            type:"post",
            url:"/",
            data:pd,
            cache:false,
            success:function(data){
                alert(data);
            },
            error:function(){
                alert("error!");
            },
        });
    });
});