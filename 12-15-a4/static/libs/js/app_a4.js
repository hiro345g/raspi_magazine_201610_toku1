$(document).ready(function(){
    //var path = '/static/graph_list_humidity.json';
    //var path = '/static/graph_list_temperature.json';
    var INTERVAL = 10000; // 10秒
    var IMAGE_LENGTH_MAX = 3;
    function refresh_image(target) {
      var img_tag_id = '#img_' + target;
      var timestamp = new Date().getTime();
      $(img_tag_id).attr('src', $(img_tag_id).attr('src')+'?'+timestamp);
    }
    function refresh_image_list(target) {
      var path = '/static/graph_list_' + target + '.json';
      var img_list_tag_id = '#img_' + target + '_list';
      var status_tag_id = '#status_' + target;
      $.ajax({ url: path, type: 'GET', cache: false }).done(function(data, textStatus, jqXHR) {
        list = data['graph_list'];
        $(img_list_tag_id).empty();
        list_len = list.length;
        if (list_len > IMAGE_LENGTH_MAX) {
          list_len = IMAGE_LENGTH_MAX;
        }
        for (var i=0; i<list_len; i++) {
          var index = IMAGE_LENGTH_MAX-i-1;
          var img = $("<img>").attr("src", list[index]).attr("width",320);
          $(img_list_tag_id).append(img);
        }
        $(status_tag_id).empty();$(status_tag_id).html('success');
      })
      .fail(function(jqXHR, textStatus, errorThrown){
        $(status_tag_id).empty();$(status_tag_id).html('fail');
      })
    }
    get_image_list = function() {
      var targets = ['air_pressure', 'humidity', 'temperature'];
      for (var i=0; i<targets.length; i++) {
        refresh_image(targets[i]);
        refresh_image_list(targets[i]);
      }
    };
    get_image_list();
    timer_id = setInterval("get_image_list()", INTERVAL);
});
