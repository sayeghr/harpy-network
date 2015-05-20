$( document ).ready(function() {
    $('#prestation-table').dataTable();

    $('.prestation-row').click(function() {
        // row was clicked
        prestation_id = $(this).data("prestation-id");
        window.location.href = window.location.href + '/' + prestation_id;
    });
});