$(document).ready(function(){
    var path = '/api/data/1';
    // スライダーの値を表示
    $('#api_data_1_value').change(function(event) {
      console.log('$(\'#api_data_1_value\').val():' + $('#api_data_1_value').val());
      v = $('#api_data_1_value').val() + '';
      $('#range_value').html(v);
    });
    // GET
    $('#api_get').click(function(event){
      $.ajax({
        url: path, type: 'GET', cache: false,
        contentType: 'application/json'
      })
      .done(function(data, textStatus, jqXHR) {
        console.log(data['res'] + ', ' + data['value']);
        if (data['res'] !== 'fail') {
          var value = Number(data['value']);
          console.log(data['value'] + ' -> ' + value);
          if (0<=value && value<=100) {
            $('#api_data_1_value').val(value);
            $('#range_value').html(value+'');
            $('#status').empty(); $('#status').html('get success');
            return;
          } else {
            alert('value error:' + value);
          }
        }
        $('#status').empty();$('#status').html('get fail');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        console.log(data['res']);
        $('#status').empty();$('#status').html('get fail');
      })
    });
    // POST
    $('#api_post').click(function(event){
      var value = $('#api_data_1_value').val();
      var json_data = JSON.stringify({ 'value' : value });
      console.log('json_data:' + json_data);
      $.ajax({
        url: path, type: 'POST', cache: false,
        data: json_data, dataType: 'application/json',
        contentType: 'application/json'
      })
      .done(function(data, textStatus, jqXHR) {
        if (data['res'] === 'fail') {
          $('#status').empty();$('#status').html('post fail');
        } else {
          $('#status').empty(); $('#status').html('post success');
        }
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        var responseText = JSON.parse(jqXHR.responseText);
        if (responseText['res'] === 'ok') {
          $('#status').empty(); $('#status').html('post success');
        } else {
          $('#status').empty(); $('#status').html('post fail');
        }
      })
    });
    // PUT
    $('#api_put').click(function(event){
      var value = $('#api_data_1_value').val();
      var json_data = JSON.stringify({ 'value' : value });
      console.log('json_data:' + json_data);
      $.ajax({
        url: path, type: 'PUT', cache: false,
        data: json_data, dataType: 'application/json',
        contentType: 'application/json'
      })
      .done(function(data, textStatus, jqXHR) {
        if (data['res'] === 'fail') {
          $('#status').empty();$('#status').html('put fail');
        } else {
          $('#status').empty(); $('#status').html('put success');
        }
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        var responseText = JSON.parse(jqXHR.responseText);
        if (responseText['res'] === 'ok') {
          $('#status').empty(); $('#status').html('put success');
        } else {
          $('#status').empty(); $('#status').html('put fail');
        }
      })
    });
    // DELETE
    $('#api_delete').click(function(event){
      var json_data = JSON.stringify({ 'value' : '' });
      $.ajax({
        url: path, type: 'DELETE', cache: false,
        data: json_data, dataType: 'application/json',
        contentType: 'application/json'
      })
      .done(function(data, textStatus, jqXHR) {
        var responseText = jqXHR.responseText;
        if (responseText === '') {
          $('#status').empty(); $('#status').html('delete success');
          $('#api_data_1_value').val(0);
          $('#range_value').html('0');
        } else {
          $('#status').empty();$('#status').html('delete fail');
        }
      })
      .fail(function(jqXHR, textStatus, errorThrown){
          $('#status').empty(); $('#status').html('delete fail');
      })
    });
});
