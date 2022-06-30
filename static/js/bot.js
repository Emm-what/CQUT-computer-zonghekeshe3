
var text = $("#f-left")
var data = {}

function act()
{
    data['name'] = $("#f-left").val()
    console.log(data)
    if(text.val()==null||text.val()=="")
	{
		text.focus();
		return;
	}

	$(".b-body").append("<div class='mWord'><span></span><p>" + text.val() + "</p></div>");
	$(".b-body").scrollTop(10000000);
	var args = {
	    type:"POST",
	    url:$SCRIPT_ROOT + '/result'
	    data:{"name":text.val()}
	    contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
	    success:function(data)
	    {
	        res = $('#result').text(data.result);
	        $(".b-body").append("<div class='rotWord'><span></span> <p id='member'>" + res + "</p></div>");
	        $(".b-body").scrollTop(10000000);
	    }
	}
	text.val("");
	text.focus();

}

$("#btn").click(function()
{
	act();
});
function ajax(mJson)
{
	var type=mJson.type;
	var url=mJson.url;
	var data=mJson.data;
	var success=mJson.success;
}

