$(document).ready(function(){
    $('#running').click(function(event){
      var path = '/led_pwm_list/0/' + $('#running').val()
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#LED1').click(function(event){
      var path = '/led_pwm_list/1/' + $('#LED1').val()
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#LED2').click(function(event){
      var path = '/led_pwm_list/2/' + $('#LED2').val()
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#LED3').click(function(event){
      var path = '/led_pwm_list/3/' + $('#LED3').val()
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
});