$(document).ready(function(){
    // 状態取得
    $('[name="led_checkbox"]').click(function(event){
      // アクセスするURIのパスをラジオボタンから取得
      var path = $('[name="led_checkbox"]:checked').val()
      // jQueryのajax()関数で /led_list/[0-3] からGET
      $.ajax({
        url: path,
        type: 'GET',
        cache: false
      })
      .done(function(data, textStatus, jqXHR) {
        // 成功したらsuccess
        $('#status').empty();
        $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        // 失敗したらfail
        $('#status').empty();
        $('#status').html('fail');
      })
    });
});