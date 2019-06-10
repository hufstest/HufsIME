var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
var isEnd=false
var limit= $('#limit').val()
var temp=0
$('#callmorepost').click(function(){
            var page = $('#page').val();

            if(page > limit){
                return;
                }
//            if(page > limit){
//                return;
//                }
            callMoreArticleAjax(page);
            $('#page').val(parseInt(page)+1);

        });

        $(window).scroll(function(){
            var scrollHeight = $(window).scrollTop() + $(window).height();
            var documentHeight = $(document).height();
            if (scrollHeight = documentHeight){
            var page = $('#page').val();
            if(page > limit){
                return;
                }
            callMoreArticleAjax(page);
                $('#page').val(parseInt(page)+1);
            }


        });
        function callMoreArticleAjax(page) {

            $.ajax( {
            type : 'POST',
            url: 'scroll/',
            data: {
            'page': page,
             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:addMoreArticleAjax,
            dataType:'html'
            });

           }
        function addMoreArticleAjax(data, textStatus, jqXHR) {
//          console.log(data)
//          console.log(typeof(data))
//          console.log(data.length)
            $('#scroll').append(data);


        }




