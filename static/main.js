$(function(){
    $('#submit').click(function(){
        msg = $('#message').val();

        $('.messages').append($('<pre>').addClass('xnet').text(msg));
        $('#message').prop('disabled', true);

        $.ajax('/send', {
            method: 'post',
            data: {'msg': msg},
            success: function(res){
                $('#message').val('');
                $('.messages').append($('<pre>').addClass('snitch').text(res));
                $('#message').prop('disabled', false);
            }

        });
    });
});
