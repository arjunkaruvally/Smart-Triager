function startup()
{
	$(".button-collapse").sideNav();
}

function sanitize_json(x)
{
	x = x.replace(/False/g,'false')
	x = x.replace(/True/g,'true')
	x = x.replace(/u'/g,'"')
	x = x.replace(/'/g,'"')

	x = JSON.parse(x)

	return x	
}

function get_scheduler_status()
{
	$.ajax({
		url: '/get_scheduler_status',
		type: 'POST',
		success: function(data){
			$('#scheduler_status_span').html("["+data['status']+"]")
			if(data['date']!="" && data['date']!=undefined)
			{
				$('#report_date_span').html("["+data['date']+"]")
			}
			if($('#upload_files'))
			{
				if(data['status']=='running')
					$('#upload_files').addClass('disabled')
				else
					$('#upload_files').removeClass('disabled')
			}
		},
		error: function(data){
			Materialize.toast('Server Error',8000);
		},
		cache: false,
		contentType: false,
		processData: false
	});
}

function listen_scheduler_status(){
	var socket = io.connect('http://' + document.domain + ':5001')

	socket.on('connect', function(){
		console.log('connected')
		get_scheduler_status()
	});

	socket.on('scheduler_running_status', function(data){
		// console.log(data)
		$('#scheduler_status_span').html("["+data['status']+"]")
		if(data['date']!="" && data['date']!=undefined)
		{
			$('#report_date_span').html("["+data['date']+"]")
		}

		if($('#upload_files'))
		{
			if(data['status']=='running')
				$('#upload_files').addClass('disabled')
			else
				$('#upload_files').removeClass('disabled')
		}
		
	});

	socket.on('disconnect', function(){
		console.log('disconnected')
	});

}