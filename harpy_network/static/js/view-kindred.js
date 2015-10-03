$( document ).ready(function() {
    $('#status-table').dataTable( {
            "drawCallback": function( settings ) {
                updateStatusTableLinks();
            }
    });
});

function updateStatusTableLinks() {
    $('.status-row').click(function() {
        // row was clicked
        status_id = $(this).data("status-id");
        window.location.href = /kindred/ + kindredID + '/status/' + status_id;
    });
}