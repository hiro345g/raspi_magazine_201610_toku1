$(document).ready(function(){
    $('#led_on').click(function(event){
      var path = '/led/1'
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#led_off').click(function(event){
      var path = '/led/0'
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('[name="led_checkbox"]').click(function(event){
      var path = $('[name="led_checkbox"]:checked').val()
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#matrix0').click(function(event){
      var path = '/matrix/0'
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#matrix1').click(function(event){
      var path = '/matrix/1'
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#matrix2').click(function(event){
      var path = '/matrix/2'
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#matrix3').click(function(event){
      var path = '/matrix/3'
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
    $('#pattern').change(function(event){
      var path = $('#pattern').val()
      if (path === '') {
        return
      }
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
});
