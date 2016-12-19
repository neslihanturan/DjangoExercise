
$('.likes-button').click(function(){
    var postid;
    postid = $(this).attr("data-postid");
            $.get('/freequestion/upvote/', {post_id: postid}, function(data){

        $('#'+postid).html(data);
    $("#" + $(this).attr("name")).hide();
});
});
