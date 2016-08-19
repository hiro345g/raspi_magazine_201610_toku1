$(document).ready(function(){
    // 一覧取得
    $('#get_entries').click(function(event){
      // jQueryのajax()関数で /entries からGET
      $.ajax({
        url: '/json/1',
        type: 'GET',
        cache: false
      })
      .done(function(data, textStatus, jqXHR) {
        // 成功したら一覧を更新
        $('#table_air_pressure_entries').empty();
        var air_pressure_list = data['air_pressure_list']
        $('#table_air_pressure_entries').append('<tr><th>id</th><th>created_datetime</th><th>value</th></tr>')
        for(var i in air_pressure_list){
          $('#table_air_pressure_entries').append('<tr><td>' + air_pressure_list[i]['id'] + '</td><td>' + air_pressure_list[i]['created_datetime'] + '</td><td>' + air_pressure_list[i]['value'] + '</td>');
        }
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        alert('fail');
      })
    });
});
