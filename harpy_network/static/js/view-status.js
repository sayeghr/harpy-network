$( document ).ready(function() {
    $("#remove-status").on("click", function(e) {
        bootbox.dialog({
          message: "Are you sure you want to remove this status? This cannot be undone.",
          title: "Remove Status",
          buttons: {
            cancel: {
              label: "Cancel",
              className: "btn-primary",
              callback: function() {
              }
            },
            remove: {
              label: "Remove",
              className: "btn-danger",
              callback: function() {
                $.ajax({
                    url: '#',
                    type: 'DELETE',
                    success: function(result) {
                        // We have successfully deleted, now we redirect.
                        if (result.redirect) {
                            window.location = result.redirect;
                        }
                    }
                });

              }
            },
          }
        });
    });
});
