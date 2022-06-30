$("#btn").click(function()
{
	var text = $("#f-left")
	var dat = {'name':text.val()}
	if(text.val()==null||text.val()=="")
	{
		text.focus();
		return;
	}

	$(".b-body").append("<div class='mWord'><span></span><p>" + text.val() + "</p></div>");
	$(".b-body").scrollTop(10000000);

	$.ajax({
    type: 'get',
    url: '/result',
    data: dat,
    contentType: 'application/json; charset=UTF-8',
    dataType: 'json',
    success: function(data) {
        $.getJSON('/result',function(res)
        {
            var h = res.a
            $(".b-body").append("<div class='rotWord'><span></span> <p id='member'>" + h + "</p></div>");
	        $(".b-body").scrollTop(10000000);
        })
    }
    })

    text.val("");
})
