$( document ).ready(function() {
    $('#debtor-id').select2({
        placeholder: "Select a Kindred",
        allowClear: true
    });
    $('#creditor-id').select2({
        placeholder: "Select a Kindred",
        allowClear: true
    });
    $('#boon-weight').select2({
        placeholder: "Select a Boon Weighting",
        allowClear: true
    });
});