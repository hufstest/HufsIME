 $(".like").click(function(){
    var pk = $(this).attr('name')
    $.ajax({
      type: "POST",
      url: "like/",
      data: {'pk': pk, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      dataType: "json",

     success: function(response){
        id = $(this).attr('name')
        $('#count'+ pk).html("count : "+ response.likes_count);
        alert(response.message);
        // alert("좋아요수 :" + response.likes_count);
      },
      error:function(request,status,error){
        alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
      }









  });
})
