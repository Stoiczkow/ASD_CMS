setInterval(function() {
        var button = $('#alertbtn')
            $.ajax({
                type: 'GET',
                url: '/current_interruptions',
                success: function(data){
                    if( data['alert'] == true){
                        button.trigger('click');
                    };
                }
            });
        }, 1000 * 60 * 1);