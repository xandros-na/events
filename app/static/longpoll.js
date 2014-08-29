function longpoll() {
    var latest = String($('span').first().attr('id'));
    $.ajax({
        type: "GET",
        url: $SCRIPT_ROOT + '/update', 
        async: true,
        dataType: 'json',
        timeout: 10000,

        success: function(data) {
            console.log('success');

            var data_id = parseInt(data.id);
            if (data_id != -1) { // check if database is empty 
                var to_str = String(data_id);
                var h2_id = document.getElementById(to_str);
                    
                if (data.deleted) {
                    $('span[id=' + data.id + ']').hide();                    
                    $('span[id=p' + data.id + ']').hide();                    
                } else {

                    if (h2_id != null) { // check if there is an id with data_id 
                    } else {

                        if (! $('#data.id').length) { // check if this an already existing tag with this id
                            $('#em').hide();
                            // converts datestring and populates the newer/edited events
                            var dateString = data.thedate;
                            dateString = dateString.replace(/-/g, ' ');
                            dateString = dateString.replace(/GMT/g, ' ');
                            var d = new Date(dateString);

                            $('#marker').after('<span id=' + data.id + '><h2>' + data.title + '</h2><span id="p' + data.id + '"<p>' + data.room + '<br>' + d.toDateString() + ', ' + d.toLocaleTimeString() + '</p></span>');

                            if (data.replaced_id != -1) { // removes the edited event using replaced_id
                                $('span[id=' + data.replaced_id + ']').remove();
                                $('span[id=p' + data.replaced_id + ']').remove();
                            }
                        }
                    }
                }
            } 
            setTimeout(longpoll, 10000);
        } //end success
    }); // end ajax
}
    
$(document).ready(function() {
    longpoll();
});

