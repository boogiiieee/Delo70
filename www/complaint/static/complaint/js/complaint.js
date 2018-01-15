$(function(){	
	$(".bttn_send").click(function(){
		var text = $('#id_message').val();
		if(text != "")			
		{		
			if(text.length > 200)
			{
				$('.input_error').text("Длина сообщения не должна превышать 200 символов.");	
				$('.modal-body').addClass('error-block');				
			}	
			else
			{
				var url = window.location.href;
				var all = $('#complaint_form').serialize();
				$.ajax({
						type: "POST",
						dataType: 'json',
						url: '/complaint_text/',
						data: all+"&url="+url, 
						success: function(data){
							$("#id_message").val("");
							$('#complaint_form').modal('hide');
							$('.modal-body').removeClass('error-block');
							$('#complaint_thanks').modal('show');
							$('.input_error').text("");
						},
						error: function() {
							$('.input_error').text("Произошла ошибка.");
						}
					});							
			}			
		}
		else
		{
			$('.input_error').text("Обязательное поле.");
			$('.modal-body').addClass('error-block');
		}		
		return false;
	});	

});



