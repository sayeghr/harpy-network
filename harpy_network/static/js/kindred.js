$( document ).ready(function() {
    $('#kindred-table').dataTable( {
            "drawCallback": function( settings ) {
                updateKindredTableLinks();
            }
    });
});

function updateKindredTableLinks() {
    $('.kindred-row').click(function() {
        // row was clicked
        kindred_id = $(this).data("kindred-id");
        window.location.href = window.location.href + '/' + kindred_id;
    });
}