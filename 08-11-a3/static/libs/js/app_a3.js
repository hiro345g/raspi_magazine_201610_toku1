$(document).ready(function(){
    reflesh_img = function() {
      var path = '/static/100mm_photo.jpg';
      var timestamp = new Date().getTime();
      var url=$('#100mm_photo').attr('src')+'?'+timestamp;
      $('#100mm_photo').attr('src', url);
    }
    $('#select_servo').change(function(event){
      var path = $('#select_servo').val()
      if (path === '') {
        return
      }
      $.ajax({ url: path, type: 'GET', cache: false })
      .done(function(data, textStatus, jqXHR) {
        $('#status').empty(); $('#status').html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $('#status').empty();$('#status').html('fail');
      })
    });
});
