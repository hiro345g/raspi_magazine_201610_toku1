$(document).ready(function(){
    var INTERVAL = 1000;
    get_status = function() {
      var path = '/status/led';
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        if (data === '1') {
          $('#status_led').empty(); $('#status_led').html('ON');
        } else {
          $('#status_led').empty(); $('#status_led').html('OFF');
        }
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status_led').empty();$('#status_led').html('fail');
      })
      path = '/status/button';
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        if (data === '1') {
          $('#status_button').empty(); $('#status_button').html('ON');
        } else {
          $('#status_button').empty(); $('#status_button').html('OFF');
        }
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status_button').empty();$('#status_button').html('fail');
      })
    }
    get_status();
    timer_id = setInterval("get_status()", INTERVAL);
});
